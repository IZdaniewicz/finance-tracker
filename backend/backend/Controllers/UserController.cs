using Backend.Models;
using Backend.Repositories;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Threading.Tasks;

namespace Backend.Controllers
{
    [ApiController]
    public class UserController : ControllerBase
    {
        private readonly IUserRepository _userRepository;

        public UserController(IUserRepository userRepository)
        {
            _userRepository = userRepository;
        }

        [HttpGet("/users")]
        //[Authorize]
        public async Task<IActionResult> ListUsers()
        {
            var users = await _userRepository.GetAllAsync();
            return Ok(users);
        }

        [HttpGet("/users/{id:int}")]
        public async Task<IActionResult> GetUser(int id)
        {
            try
            {
                var user = await _userRepository.FindByIdAsync(id);
                if (user == null)
                {
                    return NotFound("No matching user found");
                }

                return Ok(user);
            }
            catch (Exception e)
            {
                return BadRequest(e.ToString());
            }
        }

        [HttpPut("/users/{id:int}")]
        public async Task<IActionResult> ModifyUser(int id, [FromBody] User request)
        {
            try
            {
                var user = await _userRepository.FindByIdAsync(id);
                if (user == null)
                {
                    return NotFound("No matching user found");
                }

                user.Username = request.Username;
                await _userRepository.UpdateAsync(user);

                return Ok("User updated!");
            }
            catch (Exception e)
            {
                return BadRequest(e.ToString());
            }
        }
    }
}
