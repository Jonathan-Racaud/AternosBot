using System;
using System.IO;
using System.Threading.Tasks;
using aternos.Models;

namespace aternos
{
    public class Program
    {
        public static async Task Main(string[] args)
        {
            var configuration = BotConf.LoadFromYaml("conf.yaml");
            var bot = new AternosBot(configuration.BotToken);
            await bot.StartAsync();
        }
    }
}
