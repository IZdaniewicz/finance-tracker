using System;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using System.Threading.Tasks;
using Backend.Models;
using Backend.Repositories;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using Microsoft.IdentityModel.Tokens;
using JwtRegisteredClaimNames = Microsoft.IdentityModel.JsonWebTokens.JwtRegisteredClaimNames;

namespace Backend.Controllers
{
    public class AuthController : ControllerBase
    {
        private readonly IUserRepository _userRepository;
        private readonly IConfiguration _configuration;
        private readonly IAccountRepository _accountRepository;

        public AuthController(IUserRepository userRepository, IConfiguration configuration,IAccountRepository accountRepository)
        {
            _userRepository = userRepository;
            _configuration = configuration;
            _accountRepository = accountRepository;
        }

        [HttpPost("/auth/register")]
        [AllowAnonymous]
        public async Task<IActionResult> RegisterUser([FromBody] User user)
        {
            try
            {
                await _userRepository.AddAsync(user);
                Account account = new Account();
                account.User = user;
                account.CurrentMoney = 1;
                await _accountRepository.CreateAsync(account);
                return Ok("User and account created!");
            }
            catch (Exception e)
            {
                return StatusCode(StatusCodes.Status400BadRequest, e.ToString());
            }
        }

        [HttpPost("/auth/login")]
        public async Task<IActionResult> LoginUser([FromBody] User request)
        {
            try
            {
                User user = await _userRepository.FindByUsernameAsync(request.Username);
                if (user != null)
                {
                    // create claims details based on the user information
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
    
    }
}
