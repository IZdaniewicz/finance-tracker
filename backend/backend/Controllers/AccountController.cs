using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Backend.Models;
using Backend.Repositories;

namespace Backend.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class AccountsController : ControllerBase
    {
        private readonly IAccountRepository _accountRepository;

        public AccountsController(IAccountRepository accountRepository)
        {
            _accountRepository = accountRepository;
        }

        // GET: api/accounts
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Account>>> GetAccounts()
        {
            var accounts = await _accountRepository.GetAllAsync();
            return Ok(accounts);
        }

        // GET: api/accounts/5
        [HttpGet("{id}")]
        public async Task<ActionResult<Account>> GetAccount(int id)
        {
            var account = await _accountRepository.GetByIdAsync(id);

            if (account == null)
            {
                return NotFound();
            }

            return Ok(account);
        }

        // POST: api/accounts
        [HttpPost]
        public async Task<ActionResult<Account>> CreateAccount(Account account)
        {
            await _accountRepository.CreateAsync(account);

            return CreatedAtAction(nameof(GetAccount), new { id = account.Id }, account);
        }

        // PUT: api/accounts/5
        //[HttpPut("{id}")]
        //public async Task<IActionResult> UpdateAccount(int id, Account account)
        //{
        //    if (id != account.Id)
        //    {
        //        return BadRequest();
        //    }

        //    try
        //    {
        //        await _accountRepository.UpdateAsync(account);
        //    }
        //    catch
        //    {
        //        if (!_accountRepository.GetByIdAsync(id))
        //        {
        //            return NotFound();
        //        }
        //        else
        //        {
        //            throw;
        //        }
        //    }

        //    return NoContent();
        //}

        //// DELETE: api/accounts/5
        //[HttpDelete("{id}")]
        //public async Task<IActionResult> DeleteAccount(int id)
        //{
        //    var account = await _accountRepository.GetByIdAsync(id);

        //    if (account == null)
        //    {
        //        return NotFound();
        //    }

        //    await _accountRepository.DeleteAsync(account);

        //    return NoContent();
        //}

    }
}
