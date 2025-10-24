"""
Tests for embed block helpers.
"""

import json
import pytest
from vaiz import embed_block, EmbedType


class TestEmbedBlock:
    """Test suite for embed_block helper function."""

    def test_youtube_embed_basic(self):
        """Test creating a basic YouTube embed."""
        result = embed_block(
            url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            embed_type=EmbedType.YOUTUBE
        )
        
        assert result["type"] == "embed"
        assert result["attrs"]["custom"] == 1
        assert result["attrs"]["contenteditable"] == "false"
        assert result["attrs"]["size"] == "medium"  # default
        assert result["attrs"]["isContentHidden"] is False  # default
        assert "uid" in result["attrs"]
        
        # Check content
        assert len(result["content"]) == 1
        assert result["content"][0]["type"] == "text"
        
        # Parse embed data
        embed_data = json.loads(result["content"][0]["text"])
        assert embed_data["type"] == "YouTube"
        assert embed_data["url"] == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        # YouTube should extract embed URL
        assert embed_data["extractedUrl"] == "https://www.youtube.com/embed/dQw4w9WgXcQ"

    def test_figma_embed_with_hidden_content(self):
        """Test creating a Figma embed."""
        result = embed_block(
            url="https://www.figma.com/design/sNL3kbNERHQvP9cqB3tbSG/Figma-File-Template--Community-?node-id=0-1&p=f&t=uIEJLQJDmYT74g6r-0",
            embed_type=EmbedType.FIGMA,
            size="large",
            is_content_hidden=True
        )
        
        assert result["type"] == "embed"
        assert result["attrs"]["size"] == "large"
        assert result["attrs"]["isContentHidden"] is True
        
        # Parse embed data
        embed_data = json.loads(result["content"][0]["text"])
        assert embed_data["type"] == "Figma"
        assert embed_data["url"] == "https://www.figma.com/design/sNL3kbNERHQvP9cqB3tbSG/Figma-File-Template--Community-?node-id=0-1&p=f&t=uIEJLQJDmYT74g6r-0"
        # Figma always has isContentHidden=True in data
        assert embed_data["isContentHidden"] is True
        # Check that extractedUrl is in embed format with 'file' instead of 'design'
        assert "www.figma.com/embed?embed_host=share&url=https://www.figma.com/file/" in embed_data["extractedUrl"]
        assert "/design/" not in embed_data["extractedUrl"]

    def test_vimeo_embed(self):
        """Test creating a Vimeo embed."""
        result = embed_block(
            url="https://vimeo.com/123456789",
            embed_type=EmbedType.VIMEO
        )
        
        embed_data = json.loads(result["content"][0]["text"])
        assert embed_data["type"] == "Vimeo"
        assert embed_data["url"] == "https://vimeo.com/123456789"

    def test_codesandbox_embed(self):
        """Test creating a CodeSandbox embed."""
        result = embed_block(
            url="https://codesandbox.io/s/example",
            embed_type=EmbedType.CODESANDBOX,
            size="small"
        )
        
        assert result["attrs"]["size"] == "small"
        embed_data = json.loads(result["content"][0]["text"])
        assert embed_data["type"] == "CodeSandbox"

    def test_github_gist_embed(self):
        """Test creating a GitHub Gist embed."""
        result = embed_block(
            url="https://gist.github.com/user/abc123",
            embed_type=EmbedType.GITHUB_GIST
        )
        
        embed_data = json.loads(result["content"][0]["text"])
        assert embed_data["type"] == "GitHub Gist"
        assert embed_data["url"] == "https://gist.github.com/user/abc123"
        # GitHub Gist should be transformed to data URI
        assert embed_data["extractedUrl"].startswith("data:text/html;charset=utf-8,")
        assert ".js'></script>" in embed_data["extractedUrl"]

    def test_miro_embed_with_hidden_content(self):
        """Test creating a Miro embed with hidden content."""
        result = embed_block(
            url="https://miro.com/app/board/example",
            embed_type=EmbedType.MIRO,
            is_content_hidden=True
        )
        
        embed_data = json.loads(result["content"][0]["text"])
        assert embed_data["type"] == "Miro"
        assert embed_data["isContentHidden"] is True

    def test_iframe_embed(self):
        """Test creating a generic Iframe embed."""
        result = embed_block(url="https://example.com/embed")
        
        embed_data = json.loads(result["content"][0]["text"])
        assert embed_data["type"] == "Iframe"
        assert embed_data["url"] == "https://example.com/embed"

    def test_embed_with_empty_url(self):
        """Test creating an embed with empty URL (valid use case)."""
        # For Iframe (default), empty URL should work
        result = embed_block(url="")
        
        embed_data = json.loads(result["content"][0]["text"])
        assert embed_data["url"] == ""
        assert embed_data["extractedUrl"] == ""
        assert embed_data["type"] == "Iframe"

    def test_embed_sizes(self):
        """Test all size options."""
        for size in ["small", "medium", "large"]:
            result = embed_block(
                url="https://youtube.com/example",
                embed_type=EmbedType.YOUTUBE,
                size=size
            )
            assert result["attrs"]["size"] == size

    def test_unique_uids(self):
        """Test that each embed gets a unique UID."""
        embed1 = embed_block(url="https://youtube.com/1", embed_type=EmbedType.YOUTUBE)
        embed2 = embed_block(url="https://youtube.com/2", embed_type=EmbedType.YOUTUBE)
        
        assert embed1["attrs"]["uid"] != embed2["attrs"]["uid"]

    def test_hidden_content_only_for_figma_miro(self):
        """Test that isContentHidden in data is only set for Figma and Miro."""
        # For Figma, it should ALWAYS be True in data
        figma = embed_block(
            url="https://www.figma.com/design/test/example",
            embed_type=EmbedType.FIGMA,
            is_content_hidden=False  # Even when False in attrs
        )
        figma_data = json.loads(figma["content"][0]["text"])
        assert "isContentHidden" in figma_data
        assert figma_data["isContentHidden"] is True  # Always True for Figma
        
        # For Miro, it should be in data only when specified
        miro = embed_block(
            url="https://miro.com/test",
            embed_type=EmbedType.MIRO,
            is_content_hidden=True
        )
        miro_data = json.loads(miro["content"][0]["text"])
        assert "isContentHidden" in miro_data
        assert miro_data["isContentHidden"] is True
        
        # For YouTube, it should NOT be in data (only in attrs)
        youtube = embed_block(
            url="https://youtube.com/watch?v=test",
            embed_type=EmbedType.YOUTUBE,
            is_content_hidden=True
        )
        youtube_data = json.loads(youtube["content"][0]["text"])
        assert "isContentHidden" not in youtube_data

    def test_embed_data_json_serialization(self):
        """Test that embed data is properly JSON serialized."""
        result = embed_block(
            url="https://youtube.com/тест",  # Non-ASCII characters
            embed_type=EmbedType.YOUTUBE
        )
        
        # Should not raise an exception
        embed_data = json.loads(result["content"][0]["text"])
        assert embed_data["url"] == "https://youtube.com/тест"

    def test_default_embed_type_is_iframe(self):
        """Test that default embed type is Iframe when not specified."""
        result = embed_block(url="https://example.com/embed")
        
        embed_data = json.loads(result["content"][0]["text"])
        assert embed_data["type"] == "Iframe"
        assert embed_data["url"] == "https://example.com/embed"

    def test_embed_type_enum_values(self):
        """Test that EmbedType enum has correct values."""
        assert EmbedType.YOUTUBE.value == "YouTube"
        assert EmbedType.FIGMA.value == "Figma"
        assert EmbedType.VIMEO.value == "Vimeo"
        assert EmbedType.CODESANDBOX.value == "CodeSandbox"
        assert EmbedType.GITHUB_GIST.value == "GitHub Gist"
        assert EmbedType.MIRO.value == "Miro"
        assert EmbedType.IFRAME.value == "Iframe"

    def test_youtube_url_extraction(self):
        """Test that YouTube URLs are properly extracted to embed format."""
        # Test standard watch URL
        result1 = embed_block(
            url="https://www.youtube.com/watch?v=aY9M6MKXX7Y",
            embed_type=EmbedType.YOUTUBE
        )
        embed_data1 = json.loads(result1["content"][0]["text"])
        assert embed_data1["url"] == "https://www.youtube.com/watch?v=aY9M6MKXX7Y"
        assert embed_data1["extractedUrl"] == "https://www.youtube.com/embed/aY9M6MKXX7Y"
        
        # Test youtu.be short URL
        result2 = embed_block(
            url="https://youtu.be/dQw4w9WgXcQ",
            embed_type=EmbedType.YOUTUBE
        )
        embed_data2 = json.loads(result2["content"][0]["text"])
        assert embed_data2["url"] == "https://youtu.be/dQw4w9WgXcQ"
        assert embed_data2["extractedUrl"] == "https://www.youtube.com/embed/dQw4w9WgXcQ"

    def test_figma_url_extraction(self):
        """Test that Figma URLs are properly extracted to embed format."""
        result = embed_block(
            url="https://www.figma.com/design/sNL3kbNERHQvP9cqB3tbSG/Figma-File-Template--Community-?node-id=0-1&p=f&t=uIEJLQJDmYT74g6r-0",
            embed_type=EmbedType.FIGMA
        )
        embed_data = json.loads(result["content"][0]["text"])
        
        # Original URL should be preserved
        assert embed_data["url"] == "https://www.figma.com/design/sNL3kbNERHQvP9cqB3tbSG/Figma-File-Template--Community-?node-id=0-1&p=f&t=uIEJLQJDmYT74g6r-0"
        
        # ExtractedUrl should be in embed format with 'file' instead of 'design'
        assert embed_data["extractedUrl"].startswith("https://www.figma.com/embed?embed_host=share&url=")
        assert "https://www.figma.com/file/" in embed_data["extractedUrl"]
        assert "/design/" not in embed_data["extractedUrl"]
        
        # Figma always has isContentHidden=True
        assert embed_data["isContentHidden"] is True

    def test_github_gist_url_extraction(self):
        """Test that GitHub Gist URLs are properly extracted to data URI format."""
        result = embed_block(
            url="https://gist.github.com/gdb/b6365e79be6052e7531e7ba6ea8caf23",
            embed_type=EmbedType.GITHUB_GIST
        )
        embed_data = json.loads(result["content"][0]["text"])
        
        # Original URL should be preserved
        assert embed_data["url"] == "https://gist.github.com/gdb/b6365e79be6052e7531e7ba6ea8caf23"
        
        # ExtractedUrl should be data URI with script tag
        assert embed_data["extractedUrl"].startswith("data:text/html;charset=utf-8,")
        assert "<script src='https://gist.github.com/gdb/b6365e79be6052e7531e7ba6ea8caf23.js'></script>" in embed_data["extractedUrl"]
        assert "<base target='_blank'/>" in embed_data["extractedUrl"]

    def test_non_transformed_urls(self):
        """Test that other embed types keep original URL as extractedUrl."""
        # Miro should keep original URL
        result = embed_block(
            url="https://miro.com/app/board/test",
            embed_type=EmbedType.MIRO
        )
        embed_data = json.loads(result["content"][0]["text"])
        assert embed_data["extractedUrl"] == embed_data["url"]
        
        # CodeSandbox should keep original URL
        result2 = embed_block(
            url="https://codesandbox.io/s/test",
            embed_type=EmbedType.CODESANDBOX
        )
        embed_data2 = json.loads(result2["content"][0]["text"])
        assert embed_data2["extractedUrl"] == embed_data2["url"]

