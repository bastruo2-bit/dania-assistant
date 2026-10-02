import asyncio
import os
import sys
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineTask
from pipecat.services.openai import OpenAILLMService
from pipecat.services.elevenlabs import ElevenLabsTTSService
from pipecat.transports.services.daily import DailyParams, DailyTransport

async def main():
    transport = DailyTransport(
        "dania-room",
        "tok_dummy",
        "Dania",
        DailyParams(audio_out_enabled=True, audio_in_enabled=True)
    )
    
    llm = OpenAILLMService(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o")
    tts = ElevenLabsTTSService(api_key=os.getenv("ELEVENLABS_API_KEY"), voice_id="EXaVR5kv4Fwg1gOBIfuE")
    
    pipeline = Pipeline([transport.input(), llm, tts, transport.output()])
    task = PipelineTask(pipeline)
    runner = PipelineRunner()
    
    await runner.run(task)

if __name__ == "__main__":
    asyncio.run(main())
