from sublist3r import main as sublist3r_main


def run_sublist3r(domain: str) -> list[str]:
    """Run Sublist3r and return the list of discovered subdomains."""
    return sublist3r_main(domain, 40, None, None, True, False, False, None)
