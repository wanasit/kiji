"""
Extract, find, or navigate interesting parts of the article (e.g. main content, paragraph)

The extraction should only rely on inspected information (defined in `kiji.inspection`)
and it should avoid using the underline parsed HTML information.
"""

from typing import List, Tuple, Optional, Callable, Any

from kiji.inspection import InspectedElement, InspectedPage, InspectedCodeBlock

from collections import deque


def extract_content_element(inspection: InspectedPage) -> InspectedElement:
    _, largest_size_elem, _ = _find_largest_content_size(inspection)
    return largest_size_elem


def _find_largest_content_size(
        elem: InspectedElement,
        max_distance: int = 2
) -> Tuple[float, InspectedElement, List[float]]:

    if elem.is_paragraph:
        content_size = len(elem.get_formatted_text())
        return (content_size, elem, [content_size])

    size_by_distance = [0] * max_distance
    largest_size_elem = None
    largest_size = 0

    for c in elem.children:
        c_largest_size, c_largest_size_elem, c_size_by_distance = _find_largest_content_size(c)

        for i in range(len(c_size_by_distance)):
            size_by_distance[i] += c_size_by_distance[i]

        if c_largest_size > largest_size:
            largest_size = c_largest_size
            largest_size_elem = c_largest_size_elem

    content_size = sum(size_by_distance)
    if content_size > largest_size:
        largest_size = content_size
        largest_size_elem = elem

    size_by_distance = [0] + size_by_distance[:-1]
    return largest_size, largest_size_elem, size_by_distance


def extract_paragraph_elements(
        element: InspectedElement,
        include_headers=False,
        include_images=False,
        include_code_blocks=False,
) -> List[InspectedElement]:
    paragraphs = []
    if not element.children:
        return paragraphs

    paragraphs = []
    for c in element.children:
        if c.is_inline:
            # Todo: support this later. this is un-expected for now
            continue

        if not c.is_paragraph:
            paragraphs += extract_paragraph_elements(c, include_headers=include_headers)
            continue

        if c.is_header and not include_headers:
            continue

        if c.is_image and not include_images:
            continue

        if isinstance(c, InspectedCodeBlock) and not include_code_blocks:
            continue

        paragraphs += [c]

    return paragraphs
