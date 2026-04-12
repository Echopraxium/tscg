'use strict';

const { LLMProvider } = require('./LLMProvider');

/**
 * AnthropicProvider — Claude via Anthropic API (pay-per-use, no Pro subscription needed).
 *
 * Recommended models for TSCG pipeline:
 *   claude-haiku-4-5-20251001   — fast, cheap, good for structured JSON generation
 *   claude-sonnet-4-6           — best quality for complex transdisciplinary reasoning
 *
 * Get API key: https://console.anthropic.com
 *
 * Author: Echopraxium with the collaboration of Claude AI
 */

const DEFAULT_CONFIG = {
  baseUrl:     'https://api.anthropic.com/v1',
  model:       'claude-haiku-4-5-20251001',
  temperature: 0.2,
  maxTokens:   8192,
  timeoutMs:   120_000,
  apiVersion:  '2023-06-01',
};

class AnthropicProvider extends LLMProvider {
  constructor(config = {}) {
    super({ ...DEFAULT_CONFIG, ...config });
    if (!this.config.apiKey) {
      throw new Error('AnthropicProvider requires config.apiKey');
    }
  }

  getId()   { return 'anthropic'; }
  getName() { return `Claude API — ${this.config.model}`; }
  requiresApiKey() { return true; }

  async complete(systemPrompt, userPrompt, options = {}) {
    const body = {
      model:      options.model     ?? this.config.model,
      max_tokens: options.maxTokens ?? this.config.maxTokens,
      system:     systemPrompt,
      messages: [
        { role: 'user', content: userPrompt },
      ],
    };

    // Anthropic uses top_p / temperature differently — keep low for JSON
    if (options.temperature !== undefined) {
      body.temperature = options.temperature;
    } else {
      body.temperature = this.config.temperature;
    }

    const url  = `${this.config.baseUrl}/messages`;
    const resp = await this._fetch(url, body);

    // Anthropic returns content as array of blocks
    const textBlock = resp.content?.find(b => b.type === 'text');
    if (!textBlock) throw new Error('AnthropicProvider: no text block in response');
    return textBlock.text;
  }

  async isAvailable() {
    try {
      // Minimal check: send a 1-token request
      const body = {
        model:      this.config.model,
        max_tokens: 1,
        messages:   [{ role: 'user', content: 'ping' }],
      };
      const resp = await this._fetch(`${this.config.baseUrl}/messages`, body);
      if (resp.type === 'error') {
        return { ok: false, message: `Anthropic: ${resp.error?.message ?? 'unknown error'}` };
      }
      return { ok: true, message: `Claude API ready — model: ${this.config.model}` };
    } catch (err) {
      const msg = err.message ?? '';
      if (msg.includes('401')) return { ok: false, message: 'Claude API: invalid API key.' };
      return { ok: false, message: `Claude API not reachable: ${msg}` };
    }
  }

  // ── private ────────────────────────────────────────────────────────────────

  async _fetch(url, body) {
    const resp = await fetch(url, {
      method:  'POST',
      headers: {
        'Content-Type':      'application/json',
        'x-api-key':         this.config.apiKey,
        'anthropic-version': this.config.apiVersion,
      },
      body:   JSON.stringify(body),
      signal: AbortSignal.timeout(this.config.timeoutMs),
    });
    if (!resp.ok) {
      const text = await resp.text().catch(() => '');
      throw new Error(`Anthropic API error ${resp.status}: ${text}`);
    }
    return resp.json();
  }
}

module.exports = { AnthropicProvider };
