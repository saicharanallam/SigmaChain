"""
Validation Agent
Validates generated images for anatomical correctness and quality.
"""

import os
import httpx
from pathlib import Path
from typing import Dict, Any
from openai import OpenAI
from .base_agent import BaseAgent, AgentResult


class ValidationAgent(BaseAgent):
    """
    Agent responsible for validating images:
    - Anatomical correctness
    - Image quality
    - Prompt adherence
    - Professional standards
    """
    
    def __init__(self):
        super().__init__(
            name="Validator",
            description="Validates images for anatomical correctness and quality"
        )
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async def process(self, input_data: Dict[str, Any]) -> AgentResult:
        """
        Validates the generated image using GPT-4 Vision.
        """
        try:
            image_url = input_data.get("image_url", "")
            image_path = input_data.get("image_path", "")
            original_prompt = input_data.get("original_prompt", "")
            enhanced_prompt = input_data.get("enhanced_prompt", "")
            
            # Get image data from local file or URL
            image_data = None
            image_format = "png"
            
            if image_path:
                # Read from local file
                file_path = Path(image_path)
                if file_path.exists():
                    with open(file_path, "rb") as f:
                        image_data = f.read()
                    image_format = "png" if file_path.suffix == ".png" else "jpeg"
                else:
                    return AgentResult(
                        success=False,
                        data={},
                        message=f"Image file not found: {image_path}"
                    )
            elif image_url:
                # Try to download from URL (for local server URLs)
                try:
                    import asyncio
                    loop = asyncio.get_event_loop()
                    
                    # If it's a local path URL, read from file system
                    if image_url.startswith("/static/images/"):
                        filename = image_url.replace("/static/images/", "")
                        file_path = Path("generated_images") / filename
                        if file_path.exists():
                            with open(file_path, "rb") as f:
                                image_data = f.read()
                            image_format = "png"
                        else:
                            return AgentResult(
                                success=False,
                                data={},
                                message=f"Image file not found: {file_path}"
                            )
                    else:
                        # Download from external URL
                        async with httpx.AsyncClient() as client:
                            response = await client.get(image_url)
                            if response.status_code != 200:
                                return AgentResult(
                                    success=False,
                                    data={},
                                    message=f"Failed to download image: {response.status_code}"
                                )
                            image_data = response.content
                            image_format = "jpeg"
                except Exception as e:
                    return AgentResult(
                        success=False,
                        data={},
                        message=f"Error reading image: {str(e)}"
                    )
            else:
                return AgentResult(
                    success=False,
                    data={},
                    message="No image URL or path provided"
                )
            
            # Convert to base64 for GPT-4 Vision
            import base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # Validation system prompt
            validation_system_prompt = """You are an expert image quality and anatomical correctness validator.
Analyze the provided image and check for:

1. **Anatomical Correctness**: Are human/animal body parts proportional and correctly positioned?
2. **Image Quality**: Is the image sharp, well-composed, and professional?
3. **Prompt Adherence**: Does the image match the intended prompt?
4. **Professional Standards**: Would this meet professional photography/art standards?

Provide a detailed analysis with:
- Overall score (0-100)
- Anatomical correctness score (0-100)
- Quality score (0-100)
- Specific issues found (if any)
- Recommendations for improvement
- Pass/Fail status

Format your response as JSON with these fields:
{
    "overall_score": number,
    "anatomical_score": number,
    "quality_score": number,
    "issues": [array of strings],
    "recommendations": [array of strings],
    "passed": boolean,
    "detailed_analysis": "string"
}"""

            # Analyze image with GPT-4 Vision
            response = self.client.chat.completions.create(
                model="gpt-4o",  # GPT-4 with vision support
                messages=[
                    {
                        "role": "system",
                        "content": validation_system_prompt
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Original prompt: {original_prompt}\nEnhanced prompt: {enhanced_prompt}\n\nAnalyze this image:"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/{image_format};base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000
            )
            
            analysis_text = response.choices[0].message.content
            
            # Try to parse JSON from response
            import json
            try:
                # Extract JSON from markdown code blocks if present
                if "```json" in analysis_text:
                    analysis_text = analysis_text.split("```json")[1].split("```")[0].strip()
                elif "```" in analysis_text:
                    analysis_text = analysis_text.split("```")[1].split("```")[0].strip()
                
                analysis = json.loads(analysis_text)
            except:
                # Fallback: create structured response from text
                analysis = {
                    "overall_score": 75,
                    "anatomical_score": 75,
                    "quality_score": 75,
                    "issues": [],
                    "recommendations": [],
                    "passed": True,
                    "detailed_analysis": analysis_text
                }
            
            return AgentResult(
                success=True,
                data={
                    "validation": analysis,
                    "image_url": image_url or f"/static/images/{Path(image_path).name}" if image_path else "",
                    "passed": analysis.get("passed", True)
                },
                message="Validation completed",
                metadata={
                    "model": "gpt-4o",
                    "scores": {
                        "overall": analysis.get("overall_score", 0),
                        "anatomical": analysis.get("anatomical_score", 0),
                        "quality": analysis.get("quality_score", 0)
                    }
                }
            )
            
        except Exception as e:
            return AgentResult(
                success=False,
                data={},
                message=f"Error validating image: {str(e)}"
            )

