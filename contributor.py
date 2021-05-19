"""Here are all Contributor listed"""

__all__ = (
    "print_contributor",
    "AlbertUnruh",
    "Nxnx0502",
    "MikeCodes2586",
    "RedstoneCraft"
)


# for PyCharm
# noinspection PyShadowingBuiltins
class Contributor:
    """is the class for a Contributor"""

    # this is a link to all Contributors
    contributors = []

    def __init__(self, id: int, name: str, github: str):
        self._id = id
        self._name = name
        self._github = github
        self.contributors.append(self)

    @property
    def id(self) -> int:
        """is the Discord ID from a Contributor"""
        return self._id

    @property
    def name(self) -> str:
        """is the Discord Username from a Contributor"""
        return self._name

    @property
    def github(self) -> str:
        """is the GitHub URL from a Contributor"""
        return self._github


AlbertUnruh = Contributor(**{
    "id": 546320163276849162,
    "name": "AlbertUnruh#3643",
    "github": "https://github.com/AlbertUnruh"
})

Nxnx0502 = Contributor(**{
    "id": 752762890288758784,
    "name": "꧁☆ℕ𝕩𝕟𝕩☆꧂#9288",
    "github": "https://github.com/Nxnx0502"
})

MikeCodes2586 = Contributor(**{
    "id": 617040642106720287,
    "name": "ui-xb#6606",
    "github": "https://github.com/MikeCodes2586"
})

RedstoneCraft = Contributor(**{
    "id": 596281573582831616,
    "name": "RΞD_SΤΘΝΞ_CRΛFT#1800",
    "github": "https://github.com/RedstoneCraft"
})


def print_contributor():
    """prints all Contributors to the cmd"""

    print("Special thanks to our contributors:")
    for contributor in Contributor.contributors:
        print(f"  - {contributor.github:40}{contributor.name}")
    print("\n")