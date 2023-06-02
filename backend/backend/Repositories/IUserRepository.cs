using Backend.Models;

namespace Backend.Repositories;

public interface IUserRepository
{
    public void Add(User u);

    public IEnumerable<User> GetAll();

    public User FindById(int id);

    public User FindByUsername(string username);

    public void Update(User u);

    public void Delete(User u);
}