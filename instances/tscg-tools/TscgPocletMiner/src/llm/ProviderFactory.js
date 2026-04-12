'use strict';

const { OllamaProvider    } = require('./OllamaProvider');
const { GeminiProvider    } = require('./GeminiProvider');
const { DeepSeekProvider  } = require('./DeepSeekProvider');
const { AnthropicProvider } = require('./AnthropicProvider');

/**
 * ProviderFactory — Creates LLMProvider instances from a config object.
 *
 * 4 backends available (in recommended order for TSCG users):
 *   1. gemini    — Google Gemini Free Tier (best free cloud option)
 *   2. ollama    — Local LLM via Ollama (free, offline)
 *   3. deepseek  — DeepSeek Cloud API (pay-per-use, ~0.01€/session)
 *   4. anthropic — Claude API (pay-per-use, ~0.05€/session)
 *
 * Config example (stored in Electron userData as llm_config.json):
 * {
 *   "active": "gemini",
 *   "tscgRepoRoot": "E:\\...\\tscg",
 *   "providers": {
 *     "gemini":    { "apiKey": "AIza...", "model": "gemini-2.5-flash" },
 *     "ollama":    { "model": "phi3.5:3.8b-mini-instruct-q4_K_M" },
 *     "deepseek":  { "apiKey": "sk-..." },
 *     "anthropic": { "apiKey": "sk-ant-...", "model": "claude-haiku-4-5-20251001" }
 *   }
 * }
 *
 * Author: Echopraxium with the collaboration of Claude AI
 */

// ── Registry ──────────────────────────────────────────────────────────────────

const REGISTRY = {
  gemini:    GeminiProvider,
  ollama:    OllamaProvider,
  deepseek:  DeepSeekProvider,
  anthropic: AnthropicProvider,
};

// ── UI metadata (shown in the provider selector panel) ────────────────────────

const PROVIDER_META = {
  gemini: {
    label:       'Google Gemini (Free)',
    description: 'Gratuit, sans carte bancaire — 250 req/jour avec Gemini 2.5 Flash',
    icon:        '🆓',
    requiresKey: true,
    keyLabel:    'Google AI Studio API Key',
    quality:     '⭐⭐⭐⭐',
    speed:       'rapide',
    cost:        'Gratuit',
    keyUrl:      'https://aistudio.google.com/app/apikey',
    warning:     'Données peuvent être utilisées par Google sur le tier gratuit.',
    models: [
      { value: 'gemini-2.5-flash', label: 'Gemini 2.5 Flash — 250 req/day (recommandé)' },
      { value: 'gemini-2.5-pro',   label: 'Gemini 2.5 Pro   — 100 req/day (meilleure qualité)' },
    ],
  },
  ollama: {
    label:       'Local — Ollama',
    description: 'LLM local gratuit, offline total — Phi-3.5 Mini recommandé (4 GB VRAM)',
    icon:        '🏠',
    requiresKey: false,
    keyLabel:    null,
    quality:     '⭐⭐⭐',
    speed:       '~25 tok/s',
    cost:        'Gratuit',
    keyUrl:      'https://ollama.com',
    warning:     null,
    models: [
      { value: 'phi3.5:3.8b-mini-instruct-q4_K_M', label: 'Phi-3.5 Mini 3.8B Q4 (recommandé, 4 GB VRAM)' },
      { value: 'smollm2:1.7b-instruct-q4_K_M',     label: 'SmolLM2 1.7B Q4 (ultra-léger, 1.2 GB VRAM)' },
    ],
  },
  deepseek: {
    label:       'DeepSeek Cloud API',
    description: 'Paiement à l\'usage — format OpenAI-compatible, ~0.01€/session poclet',
    icon:        '☁️',
    requiresKey: true,
    keyLabel:    'DeepSeek API Key',
    quality:     '⭐⭐⭐⭐⭐',
    speed:       'rapide',
    cost:        '~0.01€/session',
    keyUrl:      'https://platform.deepseek.com',
    warning:     null,
    models: [
      { value: 'deepseek-chat',     label: 'DeepSeek V3 (recommandé)' },
      { value: 'deepseek-reasoner', label: 'DeepSeek R1 (raisonnement avancé)' },
    ],
  },
  anthropic: {
    label:       'Claude API (Anthropic)',
    description: 'Paiement à l\'usage — Haiku (rapide) ou Sonnet (qualité max)',
    icon:        '⭐',
    requiresKey: true,
    keyLabel:    'Anthropic API Key',
    quality:     '⭐⭐⭐⭐⭐',
    speed:       'rapide',
    cost:        '~0.05€/session',
    keyUrl:      'https://console.anthropic.com',
    warning:     null,
    models: [
      { value: 'claude-haiku-4-5-20251001', label: 'Claude Haiku 4.5 (rapide, économique)' },
      { value: 'claude-sonnet-4-6',         label: 'Claude Sonnet 4.6 (qualité maximale)' },
    ],
  },
};

// ── Factory ───────────────────────────────────────────────────────────────────

class ProviderFactory {
  /**
   * Create the active provider from a full config object.
   * @param {object} config
   * @returns {LLMProvider}
   */
  static create(config) {
    const id = config.active;
    if (!id) throw new Error('ProviderFactory: config.active is missing');

    const Cls = REGISTRY[id];
    if (!Cls) {
      throw new Error(
        `ProviderFactory: unknown provider "${id}". Valid: ${Object.keys(REGISTRY).join(', ')}`
      );
    }

    return new Cls(config.providers?.[id] ?? {});
  }

  /**
   * Return metadata for all registered providers (for UI rendering).
   * @returns {object[]}
   */
  static listProviders() {
    return Object.entries(PROVIDER_META).map(([id, meta]) => ({ id, ...meta }));
  }

  /**
   * Check availability of ALL configured providers in parallel.
   * @param {object} config
   * @returns {Promise<object>}  { providerId: { ok, message } }
   */
  static async checkAll(config) {
    const checks = Object.entries(REGISTRY).map(async ([id, Cls]) => {
      const cfg = config.providers?.[id];
      if (!cfg) return [id, { ok: false, message: 'Not configured' }];
      try {
        const result = await new Cls(cfg).isAvailable();
        return [id, result];
      } catch (err) {
        return [id, { ok: false, message: err.message }];
      }
    });

    return Object.fromEntries(
      (await Promise.allSettled(checks))
        .filter(r => r.status === 'fulfilled')
        .map(r => r.value)
    );
  }

  /**
   * Default config — Gemini free tier is the default (no payment needed).
   * @returns {object}
   */
  static defaultConfig() {
    return {
      active:       'gemini',
      tscgRepoRoot: '',
      providers: {
        gemini:    { apiKey: '', model: 'gemini-2.5-flash' },
        ollama:    { model:  'phi3.5:3.8b-mini-instruct-q4_K_M' },
        deepseek:  { apiKey: '', model: 'deepseek-chat' },
        anthropic: { apiKey: '', model: 'claude-haiku-4-5-20251001' },
      },
    };
  }

  /**
   * Get UI metadata for a single provider.
   * @param {string} id
   * @returns {object|null}
   */
  static getMeta(id) {
    return PROVIDER_META[id] ?? null;
  }
}

module.exports = { ProviderFactory, PROVIDER_META };
