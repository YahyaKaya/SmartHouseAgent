from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import google
from prompts import AGENT_INSTRUCTION, SESSION_INSTRUCTION
from tools import get_weather, search_web, open_curtain, close_curtain, get_time, turn_on_yellow_light, turn_off_yellow_light, turn_on_navy_light, turn_off_navy_light
load_dotenv()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=AGENT_INSTRUCTION,
            llm=google.realtime.RealtimeModel(
            model="gemini-2.5-flash-native-audio-preview-09-2025",
            voice="Charon",
            temperature=0.8,
        ),
            tools=[
                get_time,
                get_weather,
                search_web,
                open_curtain,
                close_curtain, 
                turn_on_yellow_light, 
                turn_off_yellow_light, 
                turn_on_navy_light, 
                turn_off_navy_light
            ],

        )
        


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(),
    )

    await ctx.connect()

    await session.generate_reply(
        instructions=SESSION_INSTRUCTION,
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))