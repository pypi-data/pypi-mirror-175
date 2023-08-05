import os
from PIL import Image, ImageDraw, ImageFont


# 原理在这里: https://stackoverflow.com/questions/62910445/watermarking-pasting-rotated-text-to-empty-image

class Watermark:
    @classmethod
    def font_family(cls):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(dir_path, 'fonts', 'qnhghp.ttf')

    """
    @description: 生成水印图片，只有1个mark
    原文件 source = 'test.jpg'
    水印文字 mark = 'js.work'
    字体名称 font_family = './fonts/ali_pht_heavy.otf'
    字号大小 font_size = 20
    """

    @classmethod
    def single(cls, **kwargs):
        original_image, rotated_text_image, watermarks_image, target = cls._preprocess(**kwargs)

        original_image_size = original_image.size
        rotated_text_image_size = rotated_text_image.size
        debug = kwargs.get('debug', False)
        offset = kwargs.get('offset', (20, 20))
        position = kwargs.get('position', 'center')

        # 水印位置 center
        x, y = cls.get_position(position, original_image_size, rotated_text_image_size, offset)
        watermarks_image.paste(rotated_text_image, (x, y), rotated_text_image)

        # 合并
        result = Image.alpha_composite(original_image, watermarks_image)
        result.save(target)

        # 水印空图中添加水印文字
        watermarks_image.paste(rotated_text_image, (x, y))

        # 原图与水印图合并
        combined_image = Image.alpha_composite(original_image, watermarks_image)

        return cls._postprocess(
            combined_image=combined_image,
            target=target,
            debug=debug,
        )

    """
    @description: 生成 repeat 方式的文字水印图
    """

    @classmethod
    def multiple(cls, **kwargs):
        original_image, rotated_text_image, watermarks_image, target = cls._preprocess(**kwargs)

        original_image_size = original_image.size
        rotated_text_image_size = rotated_text_image.size
        debug = kwargs.get('debug', False)

        combined_image = original_image
        parts = 8
        offset_x = original_image_size[0] // parts
        offset_y = original_image_size[1] // parts

        start_x = original_image_size[0] // parts - rotated_text_image_size[0] // 2
        start_y = original_image_size[1] // parts - rotated_text_image_size[1] // 2

        for a in range(0, parts, 2):
            for b in range(0, parts, 2):
                x = start_x + a * offset_x
                y = start_y + b * offset_y
                # image with the same size and transparent color (..., ..., ..., 0)
                watermarks_image = Image.new(
                    'RGBA', original_image_size, (255, 255, 255, 0))
                # put text in expected place on watermarks image
                watermarks_image.paste(rotated_text_image, (x, y))
                # put watermarks image on original image
                combined_image = Image.alpha_composite(
                    combined_image, watermarks_image)

        return cls._postprocess(
            combined_image=combined_image,
            target=target,
            debug=debug,
        )

    @classmethod
    def get_position(cls, position, original, text_size, offset):
        if position == 'center':
            x = original[0] // 2 - text_size[0] // 2
            y = original[1] // 2 - text_size[1] // 2
        elif position == 'south_east':
            x = original[0] - text_size[0] - offset[0]
            y = original[1] - text_size[1] - offset[1]
        elif position == 'south_west':
            x = offset[0]
            y = original[1] - text_size[1] - offset[1]
        elif position == 'north_west':
            x = offset[0]
            y = offset[1]
        elif position == 'north_east':
            x = original[0] - text_size[0] - offset[0]
            y = offset[1]
        else:
            x = original[0] - text_size[0] - offset[0]
            y = original[1] - text_size[1] - offset[1]
        return x, y

    @classmethod
    def _preprocess(cls, **kwargs):
        # 参数处理
        original = kwargs.get('original')
        opacity = kwargs.get('opacity', 0.5)
        filename, ext = os.path.splitext(original)
        target = kwargs.get('target', f'{filename}.watermark{ext}')
        mark = kwargs.get('mark', 'js.work')
        font_family = kwargs.get('font_family', cls.font_family())
        font_size = kwargs.get('font_size', 20)
        text_color = kwargs.get('text_color', (255, 255, 255, int(255 * opacity)))
        angle = kwargs.get('angle', 45)

        # 打开原图
        original_image = Image.open(original).convert("RGBA")
        original_image_size = original_image.size

        # 字体及 bound 信息
        font = ImageFont.truetype(font_family, font_size)
        _, _, *text_size = font.getmask(mark).getbbox()

        # 计算水印位置
        text_image = Image.new('RGBA', text_size, (255, 255, 255, 0))
        text_draw = ImageDraw.Draw(text_image)
        text_draw.text((0, 0), mark, text_color, font=font)

        # 旋转水印
        rotated_text_image = text_image.rotate(angle, expand=True, fillcolor=(0, 0, 0, 0))
        watermarks_image = Image.new('RGBA', original_image_size, (255, 255, 255, 0))

        return original_image, rotated_text_image, watermarks_image, target

    @classmethod
    def _postprocess(cls, **kwargs):
        # debug 模式下，输出水印图
        combined_image = kwargs.get('combined_image')
        target = kwargs.get('target')
        debug = kwargs.get('debug')

        if debug:
            combined_image.show()

        # 保存
        combined_image.save(target)
        return combined_image, target
