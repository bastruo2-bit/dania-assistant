import asyncio
import os
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineTask, PipelineParams
from pipecat.transports.services.daily import DailyParams, DailyTransport
# استدعاء وكيل إلفن لابز ليكون هو العقل والصوت معاً
from pipecat.services.elevenlabs import ElevenLabsConversationalAgentService

async def main():
    # 1. إعداد غرفة الاتصال المرئي (التي سترتبط بـ Vidu لاحقاً)
    transport = DailyTransport(
        "dania-room",
        "tok_dummy",
        "Dania",
        DailyParams(audio_out_enabled=True, audio_in_enabled=True)
    )
    
    # 2. ربط العقل المدبر (ElevenLabs Agent)
    # ملاحظة هامة: يجب استبدال النص بين علامتي التنصيص بمعرف الوكيل الخاص بك
    agent = ElevenLabsConversationalAgentService(
        api_key=os.getenv("ELEVENLABS_API_KEY"),
        agent_id="YOUR_AGENT_ID_HERE" 
    )
    
    # 3. بناء مسار بسيط جداً: من المتصل -> إلى العقل المدبر -> ثم الرد للمتصل
    pipeline = Pipeline([transport.input(), agent, transport.output()])
    
    task = PipelineTask(pipeline, PipelineParams(allow_interruptions=True))
    runner = PipelineRunner()
    
    await runner.run(task)

if __name__ == "__main__":
    asyncio.run(main())
