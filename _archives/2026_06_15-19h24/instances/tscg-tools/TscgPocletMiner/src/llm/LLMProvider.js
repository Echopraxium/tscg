'use strict';

/**
 * LLMProvider — Abstract base class for all LLM backends.
 *
 * All providers expose a unified interface so the rest of the app
 * is backend-agnostic. Add a new backend by subclassing this.
 *
 * Author: Echopraxium with the collaboration of Claude AI
 */
class LLMProvider {
  /**
   * @param {object} config  Backend-specific configuration
   */
  constructor(config = {}) {
    if (new.target === LLMProvider) {
      throw new Error('LLMProvider is abstract — instantiate a concrete subclass.');
    }
    this.config = config;
  }

  /**
   * Send a prompt and return the assistant's text response.
   *
   * @param {string}  systemPrompt   System / context prompt (RAG context injected here)
   * @param {string}  userPrompt     User message
   * @param {object}  [options]      Provider-specific overrides (temperature, maxTokens…)
   * @returns {Promise<string>}      Assistant text response
   */
  async complete(systemPrompt, userPrompt, options = {}) {
    throw new Error(`${this.constructor.name}.complete() not implemented`);
  }

  /**
   * Check if the backend is reachable / configured.
   * @returns {Promise<{ok: boolean, message: string}>}
   */
  async isAvailable() {
    throw new Error(`${this.constructor.name}.isAvailable() not implemented`);
  }

  /** Human-readable name shown in the UI. */
  getName() {
    throw new Error(`${this.constructor.name}.getName() not implemented`);
  }

  /** Short identifier used in config files: 'ollama' | 'deepseek' | 'anthropic' */
  getId() {
    throw new Error(`${this.constructor.name}.getId() not implemented`);
  }

  /**
   * Whether this backend requires an API key configured by the user.
   * @returns {boolean}
   */
  requiresApiKey() {
    return false;
  }
}

module.exports = { LLMProvider };
