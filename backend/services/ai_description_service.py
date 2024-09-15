from time import time
from typing import List, Dict

import anthropic
from anthropic.types import ContentBlock

from backend.core.config import Settings
from backend.core.logging import logger
from backend.llm_prompt_templates import MOTORCYCLE_LLM_PROMPT_TEMPLATE
from backend.schemas import VehicleBase, VehicleDetailRecommendation


class AnthropicClient:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=Settings.ANTHROPIC_API_KEY)
        self.model = "claude-3-haiku-20240307"  # claude-3-haiku-20240307, claude-3-5-sonnet-20240620
        self.system_prompt = "You are an assistant that improves motorcycle descriptions for an online motorcycle store"

    def get_ai_description(self, vehicle: VehicleBase) -> VehicleDetailRecommendation:
        prompt = self._format_prompt(vehicle)
        response = self._make_api_call(prompt)
        return self._parse_response(response)

    def _make_api_call(self, prompt: str) -> str:
        logger.info(f"Making Anthropic API request for prompt: {prompt}")
        start_time = time()

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0,
                system=self.system_prompt,
                messages=[{"role": "user", "content": [{"type": "text", "text": prompt}]}]
            )

            latency = time() - start_time
            logger.info(f"Anthropic API Request Completed. Latency: {latency:.2f}s")
            logger.info(f"API Response: {response.content}")

            return self._extract_text_from_content(response.content)
        except Exception as e:
            logger.error(f"Error making Anthropic API call: {str(e)}")
            raise

    @staticmethod
    def _format_prompt(vehicle: VehicleBase) -> str:
        return MOTORCYCLE_LLM_PROMPT_TEMPLATE.format(
            year=vehicle.year,
            make=vehicle.make,
            model=vehicle.model,
            color=vehicle.color,
            odometer_miles=vehicle.odometer,
            current_description=vehicle.description or ""
        )

    @staticmethod
    def _extract_text_from_content(content: List[ContentBlock]) -> str:
        return next((block.text for block in content if block.type == "text"), "")

    @staticmethod
    def _parse_response(response: str) -> VehicleDetailRecommendation:
        response_dict = AnthropicClient._response_to_dict(response)
        logger.info(f"Parsed response dict: {response_dict}")
        return VehicleDetailRecommendation(
            make=response_dict.get('MAKE', '').strip(),
            model=response_dict.get('MODEL', '').strip(),
            color=response_dict.get('COLOR', '').strip(),
            description=response_dict.get('DESCRIPTION', '').strip()
        )

    @staticmethod
    def _response_to_dict(response: str) -> Dict[str, str]:
        response_dict = {}
        current_key = None
        current_value = []

        for line in response.split('\n'):
            line = line.strip()
            if ':' in line and line.split(':')[0] in ['MAKE', 'MODEL', 'COLOR', 'DESCRIPTION']:
                if current_key:
                    response_dict[current_key] = '\n'.join(current_value).strip()
                current_key, value = line.split(':', 1)
                current_value = [value.strip()]
            elif current_key:
                current_value.append(line)

        if current_key:
            response_dict[current_key] = '\n'.join(current_value).strip()

        return response_dict


anthropic_client = AnthropicClient()


def get_ai_description_for_vehicle(vehicle: VehicleBase) -> VehicleDetailRecommendation:
    return anthropic_client.get_ai_description(vehicle)
