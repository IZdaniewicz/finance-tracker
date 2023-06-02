using System.ComponentModel.DataAnnotations;

namespace Backend.Request
{
    public class RegisterUserRequest
    {
        [Required]
        public string Username { get; set; }

        [Required]
        public string Password { get; set; }
    }
}
