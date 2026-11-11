using System.Net.Http.Json;
using InnerVoice.Api.Models;

namespace InnerVoice.Api.Services;

public interface IPythonAiClient
{
    Task<string> GenerateChatResponseAsync(string message, List<ChatMessage> history, CancellationToken cancellationToken = default);
}

public class PythonAiClient : IPythonAiClient
{
    private readonly HttpClient _httpClient;
    private readonly ILogger<PythonAiClient> _logger;

    public PythonAiClient(HttpClient httpClient, ILogger<PythonAiClient> logger)
    {
        _httpClient = httpClient;
        _logger = logger;
    }

    public async Task<string> GenerateChatResponseAsync(string message, List<ChatMessage> history, CancellationToken cancellationToken = default)
    {
        try
        {
            var payload = new
            {
                message,
                history = history.Select(h => new { role = h.Role, content = h.Content }).ToList()
            };

            var response = await _httpClient.PostAsJsonAsync("/api/chat", payload, cancellationToken);
            if (response.IsSuccessStatusCode)
            {
                var result = await response.Content.ReadFromJsonAsync<PythonChatResponseDto>(cancellationToken: cancellationToken);
                return result?.Response ?? "Cảm ơn bạn đã chia sẻ. Mình luôn ở đây lắng nghe bạn.";
            }

            _logger.LogWarning("Python AI service returned status: {StatusCode}", response.StatusCode);
            return "Mình đang gặp chút trục trặc kỹ thuật nhưng mình vẫn ở đây lắng nghe bạn. Bạn hãy chia sẻ thêm nhé.";
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to connect to Python AI microservice");
            return "Hiện tại hệ thống AI đang khởi động lại. Nếu bạn đang cảm thấy bất an hoặc cần hỗ trợ khẩn cấp, xin vui lòng gọi ngay Tổng đài Quốc gia 111 (VN) hoặc 3114 (Pháp).";
        }
    }

    private sealed class PythonChatResponseDto
    {
        public string Response { get; set; } = string.Empty;
    }
}

