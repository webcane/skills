"""Validate single-agent artifacts and publish the reviewed article."""
import argparse
import sys
import tomllib
from pathlib import Path

from cane_learning import ROOT, STAGES, read_json, render_article, validate_links, validate_shape, write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--through', choices=STAGES, default='reviewer')
    parser.add_argument('--publish', action='store_true')
    args = parser.parse_args()
    try:
        config = tomllib.loads((ROOT / 'pipeline.toml').read_text(encoding='utf-8'))
        brief = read_json(args.directory / 'brief.json')
        projection = brief.get('projection', 'article')
        if projection not in config['projections']:
            raise ValueError('Неизвестная проекция')
        state = {}
        for role in STAGES:
            contract = config['contracts'][role]
            artifact = read_json(args.directory / (contract + '.json'))
            validate_shape(artifact, read_json(ROOT / 'schemas' / (contract + '.json')))
            validate_links(role, artifact, state, brief.get('depth', 'standard'), projection)
            state[role] = artifact
            print(f'OK {contract}')
            if role == args.through:
                break
        if args.publish:
            if args.through != 'reviewer' or state['reviewer']['verdict'] != 'pass':
                raise ValueError('Публикация требует проверки reviewer с вердиктом pass')
            (args.directory / 'article.md').write_text(
                render_article(state['writer'], state['designer']), encoding='utf-8'
            )
            write_json(args.directory / 'result.json', {'status': 'published'})
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(error, file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
