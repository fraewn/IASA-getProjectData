# imports
from pydriller import RepositoryMining

# class responsible for retreiving data from git repository
class GetRepositoryData:

    def getRepInfo(self, filename, path):
        with open(filename, 'w', newline='') as f:
            f.write(f"filename;developer;commitdate;path;"
                    f"changetype\n")
            for commit in RepositoryMining(path).traverse_commits():
                # for all modifications happened in one commit do
                for m in commit.modifications:
                    f.write(f"{m.filename};{commit.author.name};"
                            f"{commit.author_date};{m.new_path};"
                            f"{m.change_type}\n")

