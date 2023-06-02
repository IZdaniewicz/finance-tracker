using Backend.Models;
using Microsoft.EntityFrameworkCore;

namespace Backend;

public class DataContext : DbContext
{
    protected readonly IConfiguration Configuration;

    public DataContext(IConfiguration configuration)
    {
        Configuration = configuration;
    }

    protected override void OnConfiguring(DbContextOptionsBuilder options)
    {
        options.UseNpgsql(Configuration.GetConnectionString("WebApiDatabase"));
    }
    
    public DbSet<User> Users { get; set; }
    public DbSet<Account> Accounts{ get; set; }
    public DbSet<Transaction> Transactions{ get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
    }


}