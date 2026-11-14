using InnerVoice.Domain.Entities;
using Microsoft.EntityFrameworkCore;

namespace InnerVoice.Application.Common.Interfaces;

public interface IAppDbContext
{
    DbSet<ConversationLog> ConversationLogs { get; }
    Task<int> SaveChangesAsync(CancellationToken cancellationToken = default);
}
