"""subfinder.enum: JSONL validado, sin proveedores externos habilitados en el lab."""
from __future__ import annotations

import json
import subprocess
from typing import Any

from harness.adapters.common import Runner
from harness.adapters.recon_common import LIMITER, RateLimiter, checked_target, profile_for
from harness.asset_graph import normalize_asset
from harness.contracts import Action, Phase, ScopeToken


def build_argv(target: str, profile: dict[str, Any]) -> list[str]:
    from harness.adapters.common import validate_target
    p = profile_for('subfinder', profile)
    return ['subfinder', '-d', validate_target(target), '-oJ', '-silent', '-duc',
            '-rl', str(p['rate_limit_rps']), '-timeout', str(p['timeout_s'])]


class SubfinderEnum:
    name = 'subfinder.enum'
    allowed_phases = (Phase.RECON,)
    destructive = False

    def __init__(self, runner: Runner | None = None, profile: dict[str, Any] | None = None,
                 limiter: RateLimiter = LIMITER):
        self.runner = runner
        self.profile = profile_for('subfinder', profile)
        self.limiter = limiter

    def run(self, action: Action, target: str, token: ScopeToken) -> dict[str, Any]:
        def error(code: str) -> dict[str, Any]:
            return {'status': 'ERROR', 'error': code, 'assets': [], 'capability': self.name}
        try:
            target = checked_target(target, token)
            if action.name != self.name or action.phase != Phase.RECON:
                return error('authorization')
            # subfinder usa proveedores pasivos externos. Ninguno se habilita por defecto.
            # runner inyectado permite capturas/simulaciones locales explícitas, nunca fallback a Internet.
            if self.runner is None:
                return error('local_source_required')
            argv = build_argv(target, self.profile)
            self.limiter.wait(target, self.profile['rate_limit_rps'])
            if not token.is_live():
                return error('authorization')
            raw = self.runner(argv, self.profile['timeout_s'])
            assets = []
            for line in raw.splitlines():
                if not line.strip():
                    continue
                item = json.loads(line)
                assets.append(normalize_asset({'type': 'host', 'address': item['host'],
                                               'source_tool': self.name, 'technologies': []}))
            return {'status': 'OK', 'assets': assets, 'capability': self.name, 'target': target}
        except subprocess.TimeoutExpired:
            return error('timeout')
        except FileNotFoundError:
            return error('missing')
        except subprocess.CalledProcessError:
            return error('exit')
        except (ValueError, KeyError, TypeError, AttributeError):
            return error('schema')
        except OSError:
            return error('io')
