using System.ComponentModel.DataAnnotations;

namespace Backend.Request
{
    public class TransactionCreateDro
    {
        [Required]
        public float Amount { get; set; }
        public DateTime Date { get; set; }
        public string Label { get; set; }
        public string Description { get; set; }
    }
}
