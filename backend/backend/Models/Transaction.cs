using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace Backend.Models
{
    public class Transaction
    {
        public int Id { get; set; }

        public float Amount { get; set; }

        public DateTime Date { get; set; }

        [MaxLength(100)]
        public string Label { get; set; }

        public string Description { get; set; }
        [JsonIgnore]
        public int AccountId { get; set; }
        [JsonIgnore]
        public Account Account { get; set; }

    }
}
