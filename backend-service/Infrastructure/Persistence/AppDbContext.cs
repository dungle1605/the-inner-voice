using InnerVoice.Application.Common.Interfaces;
using InnerVoice.Domain.Entities;
using Microsoft.EntityFrameworkCore;

namespace InnerVoice.Infrastructure.Persistence;

public class AppDbContext : DbContext, IAppDbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
    {
    }

    public DbSet<ConversationLog> ConversationLogs => Set<ConversationLog>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        modelBuilder.Entity<ConversationLog>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.HasIndex(e => e.SessionId);
            entity.HasIndex(e => e.Timestamp);
            entity.Property(e => e.RiskLevel)
                  .HasConversion<string>();
        });
    }
}
