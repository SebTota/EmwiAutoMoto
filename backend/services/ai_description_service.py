from time import time
from typing import List

import anthropic
from anthropic.types import ContentBlock

from backend.core.config import Settings
from backend.core.logging import logger
from backend.llm_prompt_templates import MOTORCYCLE_LLM_PROMPT_TEMPLATE
from backend.schemas import VehicleBase, VehicleAIRecommendation


class AnthropicClient:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=Settings.ANTHROPIC_API_KEY)
        self.model = "claude-3-5-sonnet-20240620"  # claude-3-haiku-20240307, claude-3-5-sonnet-20240620
        self.system_prompt = "You are an assistant that improves motorcycle descriptions for an online motorcycle store"

    def get_ai_description(self, vehicle: VehicleBase) -> VehicleAIRecommendation:
        prompt = self._format_prompt(vehicle)
        response = self._make_api_call(prompt)
        return self._parse_response(response)

    def _make_api_call(self, prompt: str) -> str:
        logger.info(f"Making Anthropic API request for prompt: {prompt}")
        start_time = time()

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            temperature=0,
            system=self.system_prompt,
            messages=[{"role": "user", "content": [{"type": "text", "text": prompt}]}]
        )

        latency = time() - start_time
        logger.info(f"Anthropic API Request Completed. Latency: {latency:.2f}s")
        logger.debug(f"API Response: {response.content}")

        return self._extract_text_from_content(response.content)

    @staticmethod
    def _format_prompt(vehicle: VehicleBase) -> str:
        return MOTORCYCLE_LLM_PROMPT_TEMPLATE.format(
            year=vehicle.year,
            make=vehicle.make,
            model=vehicle.model,
            odometer_miles=vehicle.odometer,
            current_description=vehicle.description or ""
        )

    @staticmethod
    def _extract_text_from_content(content: List[ContentBlock]) -> str:
        return next((block.text for block in content if block.type == "text"), "")

    @staticmethod
    def _parse_response(response: str) -> VehicleAIRecommendation:
        lines = response.strip().split("\n")
        make = lines[0].strip() if lines else ""
        model = lines[1].strip() if len(lines) > 1 else ""
        description = "\n".join(line.strip() for line in lines[2:] if line.strip())
        return VehicleAIRecommendation(make=make, model=model, description=description)


anthropic_client = AnthropicClient()


def get_ai_description_for_vehicle(vehicle: VehicleBase) -> VehicleAIRecommendation:
    return anthropic_client.get_ai_description(vehicle)
