using Backend.Migrations;
using Backend.Models;
using Backend.Repositories;
using Backend.Request;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace Backend.Controllers
{
    [Route("api/transactions")]
    public class TransactionController : ControllerBase
    {
        private readonly ITransactionRepository _transactionRepository;

        private readonly IAccountRepository _accountRepository;
        private readonly IUserRepository _userRepository;

        public TransactionController(ITransactionRepository transactionRepository, IAccountRepository accountRepository,IUserRepository userRepository)
        {
            _transactionRepository = transactionRepository;
            _accountRepository = accountRepository;
            _userRepository = userRepository;
        }

        [HttpGet]
        public async Task<IActionResult> GetAllTransactions()
        {
            List<Transaction> transactions = await _transactionRepository.GetAllAsync();
            return Ok(transactions);
        }

        [HttpGet("{id}")]
        public async Task<IActionResult> GetTransactionById(int id)
        {
            Transaction transaction = await _transactionRepository.GetByIdAsync(id);
            if (transaction == null)
            {
                return NotFound();
            }
            return Ok(transaction);
        }

        [HttpPost]
        [Authorize]
        public async Task<IActionResult> CreateTransaction([FromBody] TransactionCreateDro transactionDto)
        {
            try
            {
                var user = await _userRepository.GetLoggedUserAsync(Request);
                var transaction = new Transaction();
                transaction.Label = transactionDto.Label;
                transaction.Description = transactionDto.Description;
                transaction.Amount = transactionDto.Amount;
                transaction.Account = user.Account;
                transaction.AccountId = user.Account.Id;
                transaction.Date = transactionDto.Date;

                await _transactionRepository.CreateAsync(transaction);
                return Ok(transaction);
            }
            catch (Exception e)
            {
                return StatusCode(StatusCodes.Status400BadRequest, e.ToString());
            }
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateTransaction(int id, [FromBody] Transaction transaction)
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            if (id != transaction.Id)
            {
                return BadRequest("Invalid transaction ID");
            }

            try
            {
                Transaction existingTransaction = await _transactionRepository.GetByIdAsync(id);
                if (existingTransaction == null)
                {
                    return NotFound();
                }

                await _transactionRepository.UpdateAsync(transaction);
                return NoContent();
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"An error occurred while updating the transaction: {ex.Message}");
            }
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteTransaction(int id)
        {
            try
            {
                Transaction transaction = await _transactionRepository.GetByIdAsync(id);
                if (transaction == null)
                {
                    return NotFound();
                }

                await _transactionRepository.DeleteAsync(transaction);
                return NoContent();
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"An error occurred while deleting the transaction: {ex.Message}");
            }
        }
    }
}
