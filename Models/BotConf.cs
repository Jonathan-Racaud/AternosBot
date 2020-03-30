using System;
using System.IO;
using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;

namespace aternos.Models
{
    public class BotConf
    {
        [YamlMember(Alias = "bot_token", ApplyNamingConventions = false)]
        public string BotToken { get; set; }
        public AternosUser User { get; set; }
        public AternosHost Host { get; set; }

        public static BotConf LoadFromYaml(string path)
        {
            try 
            {
                using (var sr = new StreamReader(path))
                {
                    string content = sr.ReadToEnd();
                    var deserializer = new DeserializerBuilder()
                        .WithNamingConvention(CamelCaseNamingConvention.Instance)
                        .Build();
                    
                    var botConf = deserializer.Deserialize<BotConf>(content);
                    return botConf;
                }
            }
            catch (IOException e)
            {
                Console.WriteLine("The file could not be read:");
                Console.WriteLine(e.Message);
            }
            return null;
        }
    }

    public class AternosUser
    {
        public string Username { get; set; }
        public string Password { get; set; }
    }

    public class AternosHost
    {
        public string Aternos { get; set; }
        public string Server { get; set; }
    }
}
