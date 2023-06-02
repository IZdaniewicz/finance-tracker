using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace Backend.Models;

public class User
{
    [Column("id")]
    public int Id { get; set; }
    
    [Column("username")]
    public string Username { get; set; }
    [Column("password")]
    public string Password { get; set; }

    public User()
    {
    }
    public User(string username,string password)
    {
        this.Username = username;
        this.Password = password;
    }
}