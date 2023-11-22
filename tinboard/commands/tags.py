"""Tag filtering commands for the command palette."""

##############################################################################
# Python imports.
from functools import partial

##############################################################################
# Textual imports.
from textual.command import Hit, Hits, Provider

##############################################################################
# Local imports.
from ..messages import ShowAlsoTaggedWith, ShowTaggedWith


##############################################################################
class TagCommands(Provider):
    """A source of commands for filtering bookmarks by tag."""

    current_tags: list[str] = []
    """The current set of tags to draw on when setting up the commands."""

    async def search(self, query: str) -> Hits:
        """Handle a request to search for commands that match the query.

        Args:
            query: The query from the user.

        Yields:
            Command hits for the command palette.
        """
        matcher = self.matcher(query)
        for tag in self.current_tags:
            for prefix, message in (
                ("", ShowTaggedWith),
                ("Also", ShowAlsoTaggedWith),
            ):
                full_command = f"{prefix} tagged {tag}".strip().capitalize()
                if match := matcher.match(full_command):
                    yield Hit(
                        match,
                        matcher.highlight(full_command),
                        partial(self.screen.post_message, message(tag)),
                        help=f"Show all bookmarks that are {full_command.lower()}",
                    )


### tags.py ends here
