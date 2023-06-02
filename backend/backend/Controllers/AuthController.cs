using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Backend.Models;
using Backend.Repositories;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.IdentityModel.Tokens;
using JwtRegisteredClaimNames = Microsoft.IdentityModel.JsonWebTokens.JwtRegisteredClaimNames;

namespace Backend.Controllers;

public class AuthController : ControllerBase
{
    private readonly IUserRepository _userRepository;
    private readonly IConfiguration _configuration;

    public AuthController(IUserRepository userRepository, IConfiguration configuration)
    {
        _userRepository = userRepository;
        _configuration = configuration;
    }

    [HttpPost("/auth/register")]
    [AllowAnonymous]
    public IActionResult RegisterUser([FromBody] User user)
    {
        try
        {
            _userRepository.Add(user);
            return Ok("User created!");
        }
        catch (Exception e)
        {
            return StatusCode(StatusCodes.Status400BadRequest, e.ToString());
        }
    }

    [HttpPost("/auth/login")]
    public IActionResult LoginUser([FromBody] User request)
    {
        try
        {
            User user = _userRepository.FindByUsername(request.Username);
            if (user != null)
            {
                //create claims details based on the user information
                var claims = new[]
                {
                    new Claim(JwtRegisteredClaimNames.Sub, _configuration["Jwt:Subject"]),
                    new Claim(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString()),
                    new Claim(JwtRegisteredClaimNames.Iat, DateTime.UtcNow.ToString()),
                    new Claim("Username", user.Username),
                };

                var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_configuration["Jwt:Key"]));
                var signIn = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);
                var token = new JwtSecurityToken(
                    _configuration["Jwt:Issuer"],
                    _configuration["Jwt:Audience"],
                    claims,
                    expires: DateTime.UtcNow.AddMinutes(3600),
                    signingCredentials: signIn);

                return Ok(new JwtSecurityTokenHandler().WriteToken(token));
            }

            return StatusCode(StatusCodes.Status401Unauthorized, "Bad credentials");
        }
        catch (Exception e)
        {
            return StatusCode(StatusCodes.Status400BadRequest, e.ToString());
        }
    }


    [HttpGet("/users")]
    [Authorize]
    public IActionResult ListUsers()
    {
        IEnumerable<User> users = _userRepository.GetAll();
        return Ok(users);
    }


    [HttpGet("/users/{id:int}")]
    public IActionResult GetUser(int id)
    {
        User u = _userRepository.FindById(id);
        if (u is null)
        {
            return StatusCode(StatusCodes.Status404NotFound, "No matching user found");
        }

        return Ok(u);
    }

    [HttpPost("/users")]
    public IActionResult CreateUser([FromBody] User user)
    {
        try
        {
            _userRepository.Add(user);
            return Ok("User created!");
        }
        catch (Exception e)
        {
            return StatusCode(StatusCodes.Status400BadRequest, e.ToString());
        }
    }

    [HttpPut("/users/{id:int}")]
    public IActionResult ModifyUser(int id, [FromBody] User request)
    {
        try
        {
            User user = _userRepository.FindById(id);
            user.Username = request.Username;
            _userRepository.Update(user);
            return Ok("User updated!");
        }
        catch (Exception e)
        {
            return StatusCode(StatusCodes.Status400BadRequest, e.ToString());
        }
    }
}
