from collections import defaultdict
from github import Github
from github.Issue import Issue
from github.Milestone import Milestone
from github.PullRequest import PullRequest
from trello import TrelloClient


def setup(github_token, trello_key, trello_secret, oauth_token, oauth_token_secret):
    github = Github(github_token)

    trello = TrelloClient(
        api_key=trello_key,
        api_secret=trello_secret,
        token=oauth_token,
        token_secret=oauth_token_secret
    )

    return github, trello


class TrelloGitHubSynchronizer():

    labels = None
    _label_new = None
    _label_closed = None

    def _get_cards(self):
        cards = defaultdict(list)
        for card in self.board.all_cards():
            cards[card.name].append(card)

        return cards

    def __init__(self, github, trello, board_name):
        self.github = github
        self.trello = trello
        self.boards = {b.name: b for b in self.trello.list_boards()}
        self.board = self.boards[board_name]
        self.lists = {l.name: l for l in self.board.all_lists()}
        self.cards = self._get_cards()

    def get_list(self, name):
        trello_list = self.lists.get(name)
        if not trello_list:
            print("Creating new trello list {}".format(name))
            trello_list = self.board.add_list(name)
            self.lists[name] = trello_list

        return trello_list

    def get_label(self, name, color=None):
        if self.labels is None:
            print("getting labels")
            self.labels = {l.name: l for l in self.board.get_labels()}

        label = self.labels.get(name)
        if not label:
            print("creating label {}".format(name))
            label = self.board.add_label(name, color)
            self.labels[name] = label

        return label

    @property
    def label_new(self):
        if self._label_new is None:
            self._label_new = self.get_label('New', 'sky')

        return self._label_new

    @property
    def label_closed(self):
        if self._label_closed is None:
            self._label_closed = self.get_label('Closed', 'black')

        return self._label_closed

    def _issue_title(self, list_name, element):
        return '#{} Issue {}: {}'.format(list_name, element.number, element.title)

    def _pr_title(self, list_name, element):
        return '#{} Pull Request {}: {}'.format(list_name, element.number, element.title)

    def _release_title(self, list_name, element):
        return '#{} Release {}'.format(list_name, element.title)

    def get_title(self, list_name, element):
        if isinstance(element, Issue):
            return self._issue_title(list_name, element)
        elif isinstance(element, PullRequest):
            return self._pr_title(list_name, element)
        elif isinstance(element, Milestone):
            return self._release_title(list_name, element)

    def _add_card(self, trello_list, *args, **kwargs):
        card = trello_list.add_card(*args, **kwargs)
        self.cards[card.name].append(card)

    def _create_issue_card(self, trello_list, title, element):
        if not element.pull_request:
            print("Creating new Issue: {}".format(title))
            body = element.body + '\n\n' + element.html_url
            self._add_card(trello_list, title, body, [self.label_new])

    def _create_pr_card(self, trello_list, title, element):
        print("Creating new Pull Request: {}".format(title))
        body = element.body + '\n\n' + element.html_url
        self._add_card(trello_list, title, body, [self.label_new])

    def _create_release_card(self, trello_list, title, element, repo_name):
        print("Creating new Release: {}".format(title))
        url = 'https://github.com/{}/milestone/{}'.format(repo_name, element.number)
        self._add_card(trello_list, title, url, [self.label_new], element.due_on)

    def create_card(self, trello_list, title, element, repo_name):
        if isinstance(element, Issue):
            self._create_issue_card(trello_list, title, element)
        elif isinstance(element, PullRequest):
            self._create_pr_card(trello_list, title, element)
        elif isinstance(element, Milestone):
            self._create_release_card(trello_list, title, element, repo_name)

    def close_card(self, card):
        if (not card.labels) or self.label_closed not in card.labels:
            print("Closing card: {}".format(card.name))
            card.add_label(self.label_closed)
            cards = self.cards[card.name]
            index = cards.index(card)
            cards.remove(card)
            cards.insert(index, self.trello.get_card(card.id))

    def _sync(self, elements, list_name, repo_name):
        trello_list = self.get_list(list_name)
        self.cards = self._get_cards()

        for element in elements:
            title = self.get_title(list_name, element)
            cards = self.cards[title]
            for card in cards:
                if not card and element.state == 'open':
                    self.create_card(trello_list, title, element, repo_name)
                elif card and not card.closed and element.state == 'closed':
                    self.close_card(card)

    def sync(self, repo_name, list_name, pr_list_name=None):
        try:
            github_repo = self.github.get_repo(repo_name)

            print("Synchronizing {} Issues".format(repo_name))
            self._sync(github_repo.get_issues(state='all'), list_name, repo_name)

            print("Synchronizing {} Pull Requests".format(repo_name))
            self._sync(github_repo.get_pulls(state='all'), list_name, repo_name)

            print("Synchronizing {} Milestones".format(repo_name))
            self._sync(github_repo.get_milestones(state='all'), list_name, repo_name)
        except Exception:
            import traceback
            traceback.print_exc()
            raise
