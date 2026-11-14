using InnerVoice.Application.Common.Interfaces;
using InnerVoice.Application.Services;
using InnerVoice.Infrastructure.Persistence;
using InnerVoice.Infrastructure.Services;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

// 1. Infrastructure - Persistence
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlite(builder.Configuration.GetConnectionString("DefaultConnection")));

builder.Services.AddScoped<IAppDbContext>(provider =>
    provider.GetRequiredService<AppDbContext>());

// 2. Infrastructure - Services
builder.Services.AddSingleton<IPiiAnonymizer, PiiAnonymizer>();

builder.Services.AddHttpClient<IPythonAiClient, PythonAiClient>(client =>
{
    var baseUrl = builder.Configuration["AiService:BaseUrl"] ?? "http://localhost:8000";
    client.BaseAddress = new Uri(baseUrl);
    client.Timeout = TimeSpan.FromSeconds(30);
});

// 3. Application Services
builder.Services.AddScoped<IChatService, ChatService>();

// 4. WebApi - Controllers & OpenAPI (.NET 10)
builder.Services.AddControllers();
builder.Services.AddOpenApi();

// 5. CORS for Frontend Client
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll", policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyHeader()
              .AllowAnyMethod();
    });
});

var app = builder.Build();

// Auto-migrate / ensure SQLite DB schema is created
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    db.Database.EnsureCreated();
}

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}

app.UseCors("AllowAll");
app.UseHttpsRedirection();
app.MapControllers();

app.Run();
