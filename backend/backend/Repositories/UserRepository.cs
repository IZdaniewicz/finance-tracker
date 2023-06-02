using Backend.Migrations;
using Backend.Models;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using System.Collections.Generic;
using System.IdentityModel.Tokens.Jwt;
using System.Linq;
using System.Security.Claims;
using System.Threading.Tasks;

namespace Backend.Repositories
{
    public interface IUserRepository
    {
        Task AddAsync(User u);
        Task DeleteAsync(User u);
        Task<User> FindByIdAsync(int id);
        Task<User> FindByUsernameAsync(string username);
        Task<List<User>> GetAllAsync();
        Task UpdateAsync(User u);
        Task<User> GetLoggedUserAsync(HttpRequest request);
    }

    public class UserRepository : IUserRepository
    {
        private readonly DataContext _dbContext;

        public UserRepository(DataContext dbContext)
        {
            _dbContext = dbContext;
        }

        public async Task AddAsync(User u)
        {
            await _dbContext.Users.AddAsync(u);
            await _dbContext.SaveChangesAsync();
        }

        public async Task<List<User>> GetAllAsync()
        {
            return await _dbContext.Users.Include(u => u.Account).ToListAsync();
        }

        public async Task<User> FindByIdAsync(int id)
        {
            return await _dbContext.Users.Include(u => u.Account).FirstOrDefaultAsync(u => u.Id == id);
        }

        public async Task<User> FindByUsernameAsync(string username)
        {
            return await _dbContext.Users.Include(u => u.Account).SingleOrDefaultAsync(u => u.Username == username);
        }

        public async Task UpdateAsync(User u)
        {
            _dbContext.Users.Update(u);
            await _dbContext.SaveChangesAsync();
        }

        public async Task DeleteAsync(User u)
        {
            _dbContext.Users.Remove(u);
            await _dbContext.SaveChangesAsync();
        }

        public async Task<User> GetLoggedUserAsync(HttpRequest request)
        {

            string authorizationHeader = request.Headers["Authorization"];
            var token = authorizationHeader.Substring("Bearer ".Length).Trim();
            var handler = new JwtSecurityTokenHandler();
            var tokenRead = handler.ReadJwtToken(token);
            var username = tokenRead.Claims.FirstOrDefault(c => c.Type == "Username")?.Value;

            return await _dbContext.Users.Include(u=>u.Account).FirstOrDefaultAsync(u => u.Username == username);
        }
    }
}
