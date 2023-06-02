using System.ComponentModel.DataAnnotations.Schema;
using System.Text.Json.Serialization;

namespace Backend.Models
{
    public class Account
    {
        public int Id { get; set; }

        public float CurrentMoney { get; set; }

        [JsonIgnore]

        [ForeignKey("User")]
        public int UserId { get; set; }
        public virtual User User { get; set; }

        [JsonIgnore]
        public ICollection<Transaction> Transactions { get; set; }
    }
}
