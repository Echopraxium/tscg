'use strict';

const { LLMProvider } = require('./LLMProvider');

/**
 * OllamaProvider — Local LLM via Ollama (OpenAI-compatible API).
 *
 * Recommended model for Michel's hardware (4 GB VRAM + 16 GB RAM):
 *   phi3.5:3.8b-mini-instruct-q4_K_M   (~2.5 GB VRAM, full GPU)
 *   smollm2:1.7b-instruct-q4_K_M       (~1.2 GB VRAM, fastest)
 *
 * Install: https://ollama.com
 * Pull:    ollama pull phi3.5:3.8b-mini-instruct-q4_K_M
 *
 * Author: Echopraxium with the collaboration of Claude AI
 */

const DEFAULT_CONFIG = {
  baseUrl:     'http://localhost:11434',
  model:       'phi3.5:3.8b-mini-instruct-q4_K_M',
  temperature: 0.2,    // Low for structured JSON output
  maxTokens:   4096,
  timeoutMs:   120_000,
};

class OllamaProvider extends LLMProvider {
  constructor(config = {}) {
    super({ ...DEFAULT_CONFIG, ...config });
  }

  getId()   { return 'ollama'; }
  getName() { return `Ollama local — ${this.config.model}`; }
  requiresApiKey() { return false; }

  /**
   * Uses Ollama's OpenAI-compatible endpoint (/v1/chat/completions).
   * Ollama also supports JSON mode via response_format.
   */
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

    // Ask for JSON output when the caller requests it
    if (options.jsonMode) {
      body.response_format = { type: 'json_object' };
    }

    const url = `${this.config.baseUrl}/v1/chat/completions`;
    const resp = await this._fetch(url, body);
    return resp.choices[0].message.content;
  }

  async isAvailable() {
    try {
      const url  = `${this.config.baseUrl}/api/tags`;
      const resp = await fetch(url, { signal: AbortSignal.timeout(3000) });
      if (!resp.ok) return { ok: false, message: `Ollama HTTP ${resp.status}` };

      const data   = await resp.json();
      const models = (data.models ?? []).map(m => m.name);
      const found  = models.some(m => m.startsWith(this.config.model.split(':')[0]));

      if (!found) {
        return {
          ok: false,
          message: `Ollama running but model "${this.config.model}" not found.\n` +
                   `Run: ollama pull ${this.config.model}\n` +
                   `Available: ${models.join(', ') || '(none)'}`,
        };
      }
      return { ok: true, message: `Ollama ready — model: ${this.config.model}` };
    } catch (err) {
      return {
        ok: false,
        message: `Ollama not reachable at ${this.config.baseUrl}.\n` +
                 `Install Ollama from https://ollama.com and start it.`,
      };
    }
  }

  // ── private ────────────────────────────────────────────────────────────────

  async _fetch(url, body) {
    const resp = await fetch(url, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(body),
      signal:  AbortSignal.timeout(this.config.timeoutMs),
    });
    if (!resp.ok) {
      const text = await resp.text().catch(() => '');
      throw new Error(`Ollama API error ${resp.status}: ${text}`);
    }
    return resp.json();
  }
}

module.exports = { OllamaProvider };
