#!/usr/bin/env python3
"""
기본 OG 이미지 생성 스크립트
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def create_og_image():
    """기본 OG 이미지 생성"""
    # 이미지 크기 (1200x630은 OG 표준)
    width, height = 1200, 630
    
    # 그라데이션 배경 색상
    color1 = (11, 15, 22)    # --bg 다크
    color2 = (124, 137, 255) # --brand
    
    # 이미지 생성
    image = Image.new('RGB', (width, height), color1)
    draw = ImageDraw.Draw(image)
    
    # 그라데이션 효과 (간단한 radial gradient)
    for y in range(height):
        for x in range(width):
            # 중심에서의 거리 계산
            center_x, center_y = width // 2, height // 2
            distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
            max_distance = (width ** 2 + height ** 2) ** 0.5 / 2
            
            # 거리에 따른 색상 보간
            ratio = min(distance / max_distance, 1.0)
            r = int(color1[0] + (color2[0] - color1[0]) * (1 - ratio) * 0.3)
            g = int(color1[1] + (color2[1] - color1[1]) * (1 - ratio) * 0.3)
            b = int(color1[2] + (color2[2] - color1[2]) * (1 - ratio) * 0.3)
            
            if x % 4 == 0 and y % 4 == 0:  # 성능을 위해 4픽셀마다
                draw.rectangle([x, y, x+3, y+3], fill=(r, g, b))
    
    # 텍스트 추가
    try:
        # 시스템 폰트 사용 시도
        title_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 72)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 32)
    except:
        # 기본 폰트 사용
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # 제목
    title = "🧠 심리학 뉴스레터"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    title_y = height // 2 - 80
    
    draw.text((title_x, title_y), title, fill=(230, 234, 242), font=title_font)
    
    # 부제목
    subtitle = "매일 아침 자동 업데이트되는 프리미엄 심리학 뉴스 요약"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    subtitle_y = title_y + 100
    
    draw.text((subtitle_x, subtitle_y), subtitle, fill=(154, 164, 178), font=subtitle_font)
    
    # 저장
    output_path = Path("assets/og-default.png")
    image.save(output_path, "PNG", quality=95)
    print(f"✅ OG 이미지 생성 완료: {output_path}")

if __name__ == "__main__":
    create_og_image()
