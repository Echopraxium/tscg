'use strict';

const { LLMProvider } = require('./LLMProvider');

/**
 * GeminiProvider — Google Gemini via OpenAI-compatible endpoint.
 *
 * FREE TIER (no credit card required):
 *   gemini-2.5-flash  → 10 RPM / 250 RPD  (recommended for TSCG)
 *   gemini-2.5-pro    →  5 RPM / 100 RPD  (better reasoning, tighter quota)
 *
 * Get API key (free): https://aistudio.google.com/app/apikey
 *
 * NOTE: On the free tier, prompts may be used by Google to improve models.
 *       Switch to paid tier (enable billing in Google Cloud) to opt out.
 *
 * Author: Echopraxium with the collaboration of Claude AI
 */

const DEFAULT_CONFIG = {
  // OpenAI-compatible base URL for Gemini (no trailing slash)
  baseUrl:     'https://generativelanguage.googleapis.com/v1beta/openai',
  model:       'gemini-2.5-flash',   // Best free-tier option for TSCG
  temperature: 0.2,
  maxTokens:   8192,
  timeoutMs:   120_000,
};

class GeminiProvider extends LLMProvider {
  constructor(config = {}) {
    super({ ...DEFAULT_CONFIG, ...config });
    if (!this.config.apiKey) {
      throw new Error('GeminiProvider requires config.apiKey');
    }
  }

  getId()   { return 'gemini'; }
  getName() { return `Google Gemini Free — ${this.config.model}`; }
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

    // Gemini supports JSON mode via response_format (OpenAI-compatible)
    if (options.jsonMode) {
      body.response_format = { type: 'json_object' };
    }

    const resp = await this._fetch('/chat/completions', body);
    return resp.choices[0].message.content;
  }

  async isAvailable() {
    try {
      // Lightweight check: list models
      const url  = `${this.config.baseUrl}/models?key=${encodeURIComponent(this.config.apiKey)}`;
      const resp = await fetch(url, { signal: AbortSignal.timeout(5000) });

      if (resp.status === 400) return { ok: false, message: 'Gemini: invalid request (check API key format).' };
      if (resp.status === 401) return { ok: false, message: 'Gemini: invalid or expired API key.' };
      if (resp.status === 403) return { ok: false, message: 'Gemini: API key not authorized. Check Google AI Studio.' };
      if (!resp.ok)            return { ok: false, message: `Gemini HTTP ${resp.status}` };

      return {
        ok:      true,
        message: `Gemini ready — model: ${this.config.model} (free tier)`,
      };
    } catch (err) {
      return { ok: false, message: `Gemini not reachable: ${err.message}` };
    }
  }

  // ── private ────────────────────────────────────────────────────────────────

  async _fetch(endpoint, body) {
    // Gemini OpenAI-compat endpoint: API key goes in query param
    const url = `${this.config.baseUrl}${endpoint}?key=${encodeURIComponent(this.config.apiKey)}`;

    const resp = await fetch(url, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(body),
      signal:  AbortSignal.timeout(this.config.timeoutMs),
    });

    if (!resp.ok) {
      const text = await resp.text().catch(() => '');
      // Surface quota errors clearly
      if (resp.status === 429) {
        throw new Error(
          `Gemini rate limit exceeded (429).\n` +
          `Free tier: 250 req/day for Flash, 100 req/day for Pro.\n` +
          `Try again tomorrow or switch to gemini-2.5-flash.\n` +
          `Details: ${text.slice(0, 200)}`
        );
      }
      throw new Error(`Gemini API error ${resp.status}: ${text.slice(0, 300)}`);
    }

    return resp.json();
  }
}

module.exports = { GeminiProvider };
