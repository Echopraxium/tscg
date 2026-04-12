'use strict';

const { LLMProvider } = require('./LLMProvider');

/**
 * DeepSeekProvider — Cloud LLM via DeepSeek API (OpenAI-compatible).
 *
 * Recommended alternative to Claude Pro for TSCG users without subscription.
 * DeepSeek V3 offers near-Claude quality at very low cost (pay-per-use).
 *
 * Get API key: https://platform.deepseek.com
 * Pricing:     ~$0.14 / 1M input tokens, ~$0.28 / 1M output tokens
 *
 * Author: Echopraxium with the collaboration of Claude AI
 */

const DEFAULT_CONFIG = {
  baseUrl:     'https://api.deepseek.com/v1',
  model:       'deepseek-chat',   // DeepSeek V3 — best for TSCG reasoning
  temperature: 0.2,
  maxTokens:   8192,
  timeoutMs:   120_000,
};

class DeepSeekProvider extends LLMProvider {
  constructor(config = {}) {
    super({ ...DEFAULT_CONFIG, ...config });
    if (!this.config.apiKey) {
      throw new Error('DeepSeekProvider requires config.apiKey');
    }
  }

  getId()   { return 'deepseek'; }
  getName() { return `DeepSeek Cloud — ${this.config.model}`; }
  requiresApiKey() { return true; }

  async complete(systemPrompt, userPrompt, options = {}) {
    const body = {
      model:       options.model       ?? this.config.model,
      temperature: options.temperature ?? this.config.temperature,
      max_tokens:  options.maxTokens   ?? this.config.maxTokens,
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user',   content: userPrompt   },
      ],
    };

    if (options.jsonMode) {
      body.response_format = { type: 'json_object' };
    }

    const url  = `${this.config.baseUrl}/chat/completions`;
    const resp = await this._fetch(url, body);
    return resp.choices[0].message.content;
  }

  async isAvailable() {
    try {
      // Lightweight check: list models endpoint
      const resp = await fetch(`${this.config.baseUrl}/models`, {
        headers: { Authorization: `Bearer ${this.config.apiKey}` },
        signal:  AbortSignal.timeout(5000),
      });
      if (resp.status === 401) return { ok: false, message: 'DeepSeek: invalid API key.' };
      if (!resp.ok)            return { ok: false, message: `DeepSeek HTTP ${resp.status}` };
      return { ok: true, message: `DeepSeek ready — model: ${this.config.model}` };
    } catch (err) {
      return { ok: false, message: `DeepSeek not reachable: ${err.message}` };
    }
  }

  // ── private ────────────────────────────────────────────────────────────────

  async _fetch(url, body) {
    const resp = await fetch(url, {
      method:  'POST',
      headers: {
        'Content-Type':  'application/json',
        'Authorization': `Bearer ${this.config.apiKey}`,
      },
      body:   JSON.stringify(body),
      signal: AbortSignal.timeout(this.config.timeoutMs),
    });
    if (!resp.ok) {
      const text = await resp.text().catch(() => '');
      throw new Error(`DeepSeek API error ${resp.status}: ${text}`);
    }
    return resp.json();
  }
}

module.exports = { DeepSeekProvider };
