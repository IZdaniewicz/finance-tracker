using Backend.Models;
using Microsoft.EntityFrameworkCore;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace Backend.Repositories
{
    public interface ITransactionRepository
    {
        Task<List<Transaction>> GetAllAsync();
        Task<Transaction> GetByIdAsync(int id);
        Task CreateAsync(Transaction transaction);
        Task UpdateAsync(Transaction transaction);
        Task DeleteAsync(Transaction transaction);
    }

    public class TransactionRepository : ITransactionRepository
    {
        private readonly DataContext _dbContext;

        public TransactionRepository(DataContext dbContext)
        {
            _dbContext = dbContext;
        }

        public async Task<List<Transaction>> GetAllAsync()
        {
            return await _dbContext.Transactions.Include(t=>t.Account).ToListAsync();
        }

        public async Task<Transaction> GetByIdAsync(int id)
        {
            return await _dbContext.Transactions.Include(t => t.Account).FirstOrDefaultAsync(t=>t.Id == id);
        }

        public async Task CreateAsync(Transaction transaction)
        {
            _dbContext.Transactions.Add(transaction);
            await _dbContext.SaveChangesAsync();
        }

        public async Task UpdateAsync(Transaction transaction)
        {
            _dbContext.Transactions.Update(transaction);
            await _dbContext.SaveChangesAsync();
        }

        public async Task DeleteAsync(Transaction transaction)
        {
            _dbContext.Transactions.Remove(transaction);
            await _dbContext.SaveChangesAsync();
        }
    }
}
