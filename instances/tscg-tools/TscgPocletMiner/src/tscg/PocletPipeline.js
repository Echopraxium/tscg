'use strict';

const { buildPrompt } = require('./SystemPrompts');

/**
 * PocletPipeline — Orchestrates the 5-round poclet analysis wizard.
 *
 * Each round calls the active LLMProvider with:
 *   - A TSCG system prompt (round-specific)
 *   - RAG context retrieved from the local ontology corpus
 *   - The user's input or accumulated round data
 *
 * Author: Echopraxium with the collaboration of Claude AI
 */
class PocletPipeline {
  /**
   * @param {LLMProvider} provider    Active LLM backend
   * @param {RagBuilder}  ragBuilder  Built RAG index
   */
  constructor(provider, ragBuilder) {
    this._provider   = provider;
    this._rag        = ragBuilder;
    this._roundData  = {};   // accumulated data across rounds
    this._currentRound = 0;
  }

  /** Reset for a new poclet session. */
  reset() {
    this._roundData    = {};
    this._currentRound = 0;
  }

  get currentRound() { return this._currentRound; }
  get roundData()    { return { ...this._roundData }; }
  get isComplete()   { return this._currentRound >= 5; }

  /**
   * Run one pipeline round.
   *
   * @param {number} round        1-5
   * @param {string} userInput    Raw text from the user (used in round 1)
   * @param {function} [onToken] Optional streaming callback (string) — provider must support it
   * @returns {Promise<object>}   Parsed JSON result for this round
   */
  async runRound(round, userInput = '', onToken = null) {
    if (round < 1 || round > 5) throw new Error(`Invalid round: ${round}`);

    // Build RAG query from user input + accumulated system name
    const ragQuery = [
      userInput,
      this._roundData.systemName ?? '',
      this._roundData.domain     ?? '',
    ].filter(Boolean).join(' ');

    const ragContext = this._rag?.isBuilt
      ? this._rag.retrieve(ragQuery, 6)
      : '';

    // Build the prompt for this round
    const context = {
      userInput,
      systemName:  this._roundData.systemName,
      systemInfo:  this._summarizeSystemInfo(),
      asfidScores: this._roundData.asfid,
      scores: {
        asfid_mean: this._roundData.asfid_mean,
        revoi_mean: this._roundData.revoi_mean,
      },
      allRoundData: this._roundData,
    };

    const { systemPrompt, userPrompt } = buildPrompt(round, context, ragContext);

    // Call the LLM
    const rawText = await this._provider.complete(
      systemPrompt,
      userPrompt,
      { jsonMode: true, temperature: 0.1 }
    );

    // Parse JSON response (strip markdown fences if any)
    const parsed = this._parseJson(rawText, round);

    // Accumulate data
    this._mergeRoundData(round, parsed);
    this._currentRound = round;

    return parsed;
  }

  // ── private ────────────────────────────────────────────────────────────────

  _summarizeSystemInfo() {
    const d = this._roundData;
    const lines = [];
    if (d.domain)      lines.push(`Domain: ${d.domain}`);
    if (d.description) lines.push(`Description: ${d.description}`);
    if (d.attractor)   lines.push(`Attractor: ${d.attractor}`);
    if (d.poles)       lines.push(`Poles: ${d.poles.join(', ')}`);
    return lines.join('\n');
  }

  _mergeRoundData(round, parsed) {
    switch (round) {
      case 1:
        Object.assign(this._roundData, {
          systemName:  parsed.systemName,
          domain:      parsed.domain,
          description: parsed.description,
          pocletType:  parsed.pocletType,
          poles:       parsed.poles,
          attractor:   parsed.attractor,
        });
        break;
      case 2:
        Object.assign(this._roundData, {
          asfid:      parsed.asfid,
          asfid_mean: parsed.asfid_mean,
        });
        break;
      case 3:
        Object.assign(this._roundData, {
          revoi:          parsed.revoi,
          revoi_mean:     parsed.revoi_mean,
          epistemic_gap:  parsed.epistemic_gap,
          spectral_class: parsed.spectral_class,
        });
        break;
      case 4:
        Object.assign(this._roundData, {
          genericConcepts:      parsed.genericConcepts,
          knowledgeFieldCombos: parsed.knowledgeFieldCombos,
        });
        break;
      case 5:
        this._roundData.jsonld = parsed;
        break;
    }
  }

  _parseJson(text, round) {
    // Remove markdown fences ```json … ```
    const clean = text
      .replace(/^```json\s*/i, '')
      .replace(/^```\s*/,      '')
      .replace(/\s*```$/,      '')
      .trim();
    try {
      return JSON.parse(clean);
    } catch (err) {
      throw new Error(
        `Round ${round}: LLM did not return valid JSON.\n` +
        `Parse error: ${err.message}\n` +
        `Raw response (first 500 chars):\n${text.slice(0, 500)}`
      );
    }
  }
}

module.exports = { PocletPipeline };
