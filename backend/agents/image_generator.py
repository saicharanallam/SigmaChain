"""
Image Generation Agent
Generates images locally using Stable Diffusion model.
"""

import os
import base64
import uuid
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
from .base_agent import BaseAgent, AgentResult


class ImageGeneratorAgent(BaseAgent):
    """
    Agent responsible for generating images from enhanced prompts.
    Uses local Stable Diffusion model via Hugging Face Diffusers.
    """
    
    def __init__(self, model_name: str = "runwayml/stable-diffusion-v1-5", output_dir: str = "generated_images"):
        """
        Initialize image generator agent.
        
        Args:
            model_name: Hugging Face model name for Stable Diffusion
            output_dir: Directory to save generated images
        """
        super().__init__(
            name="ImageGenerator",
            description="Generates images from enhanced prompts using local Stable Diffusion model"
        )
        self.model_name = model_name
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.pipeline = None
        self.device = "cuda" if self._check_cuda() else "cpu"
    
    def _check_cuda(self) -> bool:
        """Check if CUDA is available"""
        try:
            import torch
            return torch.cuda.is_available()
        except:
            return False
    
    def _load_model(self):
        """Lazy load the Stable Diffusion model"""
        if self.pipeline is None:
            try:
                from diffusers import StableDiffusionPipeline
                import torch
                
                print(f"Loading Stable Diffusion model: {self.model_name}")
                print(f"Using device: {self.device}")
                
                # Load model with appropriate dtype based on device
                if self.device == "cuda":
                    self.pipeline = StableDiffusionPipeline.from_pretrained(
                        self.model_name,
                        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
                    )
                    self.pipeline = self.pipeline.to(self.device)
                else:
                    self.pipeline = StableDiffusionPipeline.from_pretrained(
                        self.model_name,
                        torch_dtype=torch.float32
                    )
                    self.pipeline = self.pipeline.to(self.device)
                
                # Enable memory efficient attention if available
                try:
                    self.pipeline.enable_attention_slicing()
                except:
                    pass
                
                print("Model loaded successfully")
                
            except Exception as e:
                raise Exception(f"Failed to load model: {str(e)}")
    
    async def process(self, input_data: Dict[str, Any]) -> AgentResult:
        """
        Generates an image from the enhanced prompt using local Stable Diffusion.
        """
        try:
            enhanced_prompt = input_data.get("enhanced_prompt", "")
            
            if not enhanced_prompt:
                return AgentResult(
                    success=False,
                    data={},
                    message="No enhanced prompt provided"
                )
            
            # Load model if not already loaded
            if self.pipeline is None:
                self._load_model()
            
            # Generate image
            return await self._generate_image(enhanced_prompt)
                
        except Exception as e:
            return AgentResult(
                success=False,
                data={},
                message=f"Error generating image: {str(e)}"
            )
    
    async def _generate_image(self, prompt: str) -> AgentResult:
        """Generate image using local Stable Diffusion model"""
        try:
            import asyncio
            import torch
            from PIL import Image
            
            # Run generation in executor to avoid blocking
            loop = asyncio.get_event_loop()
            
            def generate():
                # Generate image
                negative_prompt = "blurry, low quality, distorted, deformed, bad anatomy, bad proportions"
                
                with torch.no_grad():
                    image = self.pipeline(
                        prompt=prompt,
                        negative_prompt=negative_prompt,
                        num_inference_steps=50,
                        guidance_scale=7.5,
                        width=512,
                        height=512,
                    ).images[0]
                
                return image
            
            # Run generation in thread pool
            image = await loop.run_in_executor(None, generate)
            
            # Save image
            image_filename = f"{uuid.uuid4()}.png"
            image_path = self.output_dir / image_filename
            image.save(image_path, "PNG")
            
            # Create URL path (will be served by FastAPI static files)
            image_url = f"/static/images/{image_filename}"
            
            return AgentResult(
                success=True,
                data={
                    "image_url": image_url,
                    "image_path": str(image_path),
                    "prompt": prompt,
                    "provider": "local",
                    "model": self.model_name,
                    "device": self.device
                },
                message="Image generated successfully",
                metadata={
                    "model": self.model_name,
                    "provider": "local",
                    "device": self.device,
                    "filename": image_filename
                }
            )
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            return AgentResult(
                success=False,
                data={},
                message=f"Local generation error: {str(e)}\n{error_details}"
            )

