// uuid: 7f8e9d0c-1a2b-3c4d-5e6f-789012345678
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

namespace TSCG.Orchestrator
{
    // ==========================================
    // SECTION 1: API Data Models (DTOs)
    // ==========================================

    public class GeminiRequest
    {
        [JsonPropertyName("contents")]
        public List<Content> Contents { get; set; } = new List<Content>();

        [JsonPropertyName("systemInstruction")]
        public Content? SystemInstruction { get; set; }

        [JsonPropertyName("generationConfig")]
        public GenerationConfig? Config { get; set; }
    }

    public class Content
    {
        [JsonPropertyName("role")]
        public string? Role { get; set; }

        [JsonPropertyName("parts")]
        public List<Part> Parts { get; set; } = new List<Part>();
    }

    public class Part
    {
        [JsonPropertyName("text")]
        public string? Text { get; set; }
    }

    public class GenerationConfig
    {
        [JsonPropertyName("temperature")]
        public float Temperature { get; set; } = 0.7f;
    }

    public class GeminiResponse
    {
        [JsonPropertyName("candidates")]
        public List<Candidate>? Candidates { get; set; }
        
        [JsonPropertyName("error")]
        public ApiError? Error { get; set; }
    }

    public class Candidate
    {
        [JsonPropertyName("content")]
        public Content? Content { get; set; }
    }

    public class ApiError
    {
        [JsonPropertyName("code")]
        public int Code { get; set; }
        [JsonPropertyName("message")]
        public string? Message { get; set; }
        [JsonPropertyName("status")]
        public string? Status { get; set; }
    }
    
    // Pour lister les modèles (Diagnostic)
    public class ModelListResponse
    {
        [JsonPropertyName("models")]
        public List<ModelInfo>? Models { get; set; }
    }

    public class ModelInfo
    {
        [JsonPropertyName("name")]
        public string? Name { get; set; }
        [JsonPropertyName("displayName")]
        public string? DisplayName { get; set; }
    }


    // ==========================================
    // SECTION 2: Helper for Local Files
    // ==========================================

    public static class RepositoryLoader
    {
        public static string LoadCurrentDirectoryContext()
        {
            string path = Directory.GetCurrentDirectory();
            // Remonte de 3 niveaux si on est dans bin/Debug/net8.0
            string candidatePath = Path.GetFullPath(Path.Combine(path, "../../../"));
            
            if (File.Exists(Path.Combine(candidatePath, "Program.cs")))
            {
                path = candidatePath;
            }

            var sb = new StringBuilder();
            sb.AppendLine("Context: The following are the source code files of the application running this query.");
            
            var files = Directory.GetFiles(path, "*.cs", SearchOption.TopDirectoryOnly);
            
            foreach (var file in files)
            {
                sb.AppendLine($"\n--- FILE: {Path.GetFileName(file)} ---");
                sb.AppendLine(File.ReadAllText(file));
                sb.AppendLine("--- END FILE ---");
            }

            return sb.ToString();
        }
    }

    // ==========================================
    // SECTION 3: Agent & Orchestrator Logic
    // ==========================================

    public class AgentSession
    {
        public string Name { get; }
        private readonly string _systemInstruction;
        private readonly string _apiKey;
        private readonly HttpClient _httpClient;
        private readonly List<Content> _history;

        // MISE A JOUR: Utilisation de "gemini-2.5-flash" basé sur votre liste.
        // Vous pouvez aussi essayer "gemini-2.5-pro" pour plus de puissance (mais plus lent).
        private const string ModelId = "gemini-2.5-flash"; 
        
        private const string BaseUrl = "https://generativelanguage.googleapis.com/v1beta/models/";

        public AgentSession(string name, string systemInstruction, string apiKey, HttpClient httpClient)
        {
            Name = name;
            _systemInstruction = systemInstruction;
            _apiKey = apiKey;
            _httpClient = httpClient;
            _history = new List<Content>();
        }

        public async Task<string> SendMessageAsync(string userMessage)
        {
            _history.Add(new Content
            {
                Role = "user",
                Parts = new List<Part> { new Part { Text = userMessage } }
            });

            var request = new GeminiRequest
            {
                SystemInstruction = new Content
                {
                    Parts = new List<Part> { new Part { Text = _systemInstruction } }
                },
                Contents = _history,
                Config = new GenerationConfig { Temperature = 0.5f } 
            };

            string json = JsonSerializer.Serialize(request, new JsonSerializerOptions { DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull });
            var content = new StringContent(json, Encoding.UTF8, "application/json");

            string url = $"{BaseUrl}{ModelId}:generateContent?key={_apiKey}";

            try
            {
                var response = await _httpClient.PostAsync(url, content);
                string responseString = await response.Content.ReadAsStringAsync();
                
                var geminiResponse = JsonSerializer.Deserialize<GeminiResponse>(responseString);

                if (!response.IsSuccessStatusCode)
                {
                    if (geminiResponse?.Error != null)
                    {
                         return $"[API ERROR]: {geminiResponse.Error.Message} (Status: {geminiResponse.Error.Status})\n(URL: {url})";
                    }
                    return $"[HTTP ERROR {response.StatusCode}]: {responseString}";
                }

                string? aiText = geminiResponse?.Candidates?.FirstOrDefault()?.Content?.Parts?.FirstOrDefault()?.Text;

                if (string.IsNullOrEmpty(aiText)) return "[No response content]";

                _history.Add(new Content
                {
                    Role = "model",
                    Parts = new List<Part> { new Part { Text = aiText } }
                });

                return aiText;
            }
            catch (Exception ex)
            {
                return $"[EXCEPTION]: {ex.Message}";
            }
        }
    }

    public class Orchestrator
    {
        private readonly string _apiKey;
        private readonly HttpClient _httpClient;
        private readonly Dictionary<string, AgentSession> _agents;

        public Orchestrator(string apiKey)
        {
            _apiKey = apiKey;
            _httpClient = new HttpClient();
            _agents = new Dictionary<string, AgentSession>();
        }

        public void RegisterAgent(string name, string role)
        {
            _agents[name] = new AgentSession(name, role, _apiKey, _httpClient);
            Console.WriteLine($"[Orchestrator]: Agent '{name}' registered.");
        }

        public async Task<string> AskAgentAsync(string name, string message)
        {
            if (!_agents.ContainsKey(name)) return $"Agent {name} not found.";
            
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine($"\n>>> Sending to {name}...");
            Console.ResetColor();

            string response = await _agents[name].SendMessageAsync(message);

            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine($"<<< {name} says:\n{response}\n");
            Console.ResetColor();

            return response;
        }

        public async Task ListAvailableModels()
        {
            Console.WriteLine("\n--- DIAGNOSTIC: Checking available models for your API Key ---");
            string url = $"https://generativelanguage.googleapis.com/v1beta/models?key={_apiKey}";
            try 
            {
                var response = await _httpClient.GetAsync(url);
                string json = await response.Content.ReadAsStringAsync();
                var list = JsonSerializer.Deserialize<ModelListResponse>(json);
                
                if (list?.Models != null)
                {
                    Console.WriteLine($"Access confirmed! Found {list.Models.Count} models.");
                    // On n'affiche plus toute la liste pour ne pas spammer la console, 
                    // on sait que gemini-2.5-flash est dedans.
                }
                else 
                {
                    Console.WriteLine("Warning: Could not parse model list.");
                }
            }
            catch(Exception ex)
            {
                Console.WriteLine("Diagnostic failed: " + ex.Message);
            }
            Console.WriteLine("--------------------------------------------------------------\n");
        }
    }

    // ==========================================
    // SECTION 4: Main Program & Utils
    // ==========================================

    class Program
    {
        static async Task Main(string[] args)
        {
            Console.WriteLine("=== TSCP.Orchestrator Prototype (Gemini 2.5 Edition) ===");

            string apiKey = GetApiKey();
            if (string.IsNullOrWhiteSpace(apiKey)) return;

            var orchestrator = new Orchestrator(apiKey);

            // 1. Quick check
            await orchestrator.ListAvailableModels();
            
            // 2. Create Agents
            // Agent Technique
            orchestrator.RegisterAgent("DevBot", 
                "You are a Senior C# Developer. You analyze code and provide technical summaries. Be concise.");
            
            // Agent Business / Vulgarisation
            orchestrator.RegisterAgent("ManagerBot", 
                "You are a Project Manager. You explain technical concepts to business stakeholders using simple metaphors.");

            // --- SCENARIO EXECUTION ---

            Console.WriteLine("Loading local source code context...");
            string localCode = RepositoryLoader.LoadCurrentDirectoryContext();
            Console.WriteLine($"Code loaded ({localCode.Length} chars).");

            // Step 1: Technical Analysis
            string promptForDev = $"Here is the source code of a C# application:\n\n{localCode}\n\nQuestion: What does this application do technically?";
            await orchestrator.AskAgentAsync("DevBot", promptForDev);

            // Step 2: Manager Summary
            string promptForManager = $"Explain the concept of 'Orchestrator Pattern' simply.";
            await orchestrator.AskAgentAsync("ManagerBot", promptForManager);

            Console.WriteLine("\n=== DEMO COMPLETE ===");
            Console.WriteLine("Press any key to exit...");
            Console.ReadKey();
        }

        private static string GetApiKey()
        {
            string? envKey = Environment.GetEnvironmentVariable("GEMINI_API_KEY");
            if (!string.IsNullOrWhiteSpace(envKey))
            {
                Console.WriteLine("[System]: API Key loaded from environment variable.");
                return envKey;
            }

            Console.WriteLine("Please enter your Google AI Studio API Key (Input is masked):");
            StringBuilder password = new StringBuilder();
            while (true)
            {
                ConsoleKeyInfo key = Console.ReadKey(true);
                if (key.Key == ConsoleKey.Enter) { Console.WriteLine(); break; }
                else if (key.Key == ConsoleKey.Backspace) { if (password.Length > 0) { password.Remove(password.Length - 1, 1); Console.Write("\b \b"); } }
                else if (!char.IsControl(key.KeyChar)) { password.Append(key.KeyChar); Console.Write("*"); }
            }
            return password.ToString();
        }
    }
}