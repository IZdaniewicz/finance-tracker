using Backend.Models;
using Backend;
using Microsoft.EntityFrameworkCore;

public interface IAccountRepository
{
    Task<Account> GetByIdAsync(int id);
    Task<List<Account>> GetAllAsync();
    Task CreateAsync(Account account);
    Task UpdateAsync(Account account);
    Task DeleteAsync(Account account);
}

public class AccountRepository : IAccountRepository
{
    private readonly DataContext _dbContext;

    public AccountRepository(DataContext dbContext)
    {
        _dbContext = dbContext;
    }

    public async Task<Account> GetByIdAsync(int id)
    {
        return await _dbContext.Accounts
            .Include(a => a.User)
            .Include(a => a.Transactions)
            .FirstOrDefaultAsync(a => a.Id == id);
    }

    public async Task<List<Account>> GetAllAsync()
    {
        return await _dbContext.Accounts
            .Include (a => a.User)
            .Include(a => a.Transactions)
            .ToListAsync();
    }

    public async Task CreateAsync(Account account)
    {
        _dbContext.Accounts.Add(account);
        await _dbContext.SaveChangesAsync();
    }

    public async Task UpdateAsync(Account account)
    {
        _dbContext.Accounts.Update(account);
        await _dbContext.SaveChangesAsync();
    }

    public async Task DeleteAsync(Account account)
    {
        _dbContext.Accounts.Remove(account);
        await _dbContext.SaveChangesAsync();
    }
}
