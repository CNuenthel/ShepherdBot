@bot.command(name="my_first_command", description="My first command", scope=test_id)
async def my_first_command(ctx: interactions.CommandContext):
    await ctx.send("Hi There!")

@bot.command(
    name="say_something",
    description="say something!",
    scope=test_id,
    options = [
        interactions.Option(
            name="text",
            description="What you want to say",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def say_something(ctx: interactions.CommandContext, text: str):
    await ctx.send(f"You said '{text}'!")

@bot.command(
    type=interactions.ApplicationCommandType.USER,
    name="User Command",
    scope=test_id
)
async def test(ctx):
    await ctx.send(f"You have applied a command onto user {ctx.target.user.username}!")

