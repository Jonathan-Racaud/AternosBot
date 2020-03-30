using System;
using System.IO;
using System.Threading.Tasks;
using Discord;
using Discord.WebSocket;

namespace aternos.Models
{
    public class AternosCommandHandler()
    {
        public AternosCommandHandler()
        {

        }
    }

    public class AternosBot
    {
        private readonly DiscordSocketClient _client;
        private readonly AternosCommandService _commands;

        public string Token { get; private set; }

        public AternosBot(string token)
        {
            Token = token;
            _client = new DiscordSocketClient();
            _client.Log += Log;
        }

        public async Task StartAsync()
        {
            await _client.LoginAsync(TokenType.Bot, Token);
            await _client.StartAsync();
            await Task.Delay(-1);
        }

        private Task Log(LogMessage msg)
        {
            Console.WriteLine(msg.ToString());
            return Task.CompletedTask;
        }
    }
}
