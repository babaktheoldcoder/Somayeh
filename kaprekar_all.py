"""Extended Kaprekar utilities: batch testing, stats, and histogram plotting."""

import statistics
import matplotlib.pyplot as plt

KAPREKAR_CONST = "6174"


def kaprekar_once(num_str):
    """Perform one Kaprekar operation on a 4-digit string and return the next 4-digit string."""
    num_str = str(num_str).zfill(4)
    largest = ''.join(sorted(num_str, reverse=True))
    smallest = ''.join(sorted(num_str))
    return str(int(largest) - int(smallest)).zfill(4)


def is_repdigit(num_str):
    """Return True if all digits are the same (e.g., '1111')."""
    s = str(num_str).zfill(4)
    return len(set(s)) == 1


def steps_to_kaprekar(start_num, max_iter=50):
    """Return the number of iterations to reach 6174, or None if it doesn't reach within max_iter or is invalid.

    Repdigit numbers (e.g., '0000', '1111') are treated as invalid and return None.
    """
    s = str(start_num).zfill(4)
    if is_repdigit(s):
        return None
    steps = 0
    while s != KAPREKAR_CONST and steps < max_iter:
        s = kaprekar_once(s)
        steps += 1
        if s == "0000":
            return None
    if s == KAPREKAR_CONST:
        return steps
    return None


def compute_all():
    """Compute steps_to_kaprekar for all 4-digit numbers (0000–9999), excluding repdigits.

    Returns a tuple (counts_list, failures_list) where counts_list contains step counts (ints)
    and failures_list contains string representations of numbers that did not reach 6174.
    """
    counts = []
    failures = []
    for n in range(0, 10000):
        s = str(n).zfill(4)
        if is_repdigit(s):
            continue
        st = steps_to_kaprekar(s)
        if st is None:
            failures.append(s)
        else:
            counts.append(st)
    return counts, failures


def stats_and_plot(counts, out_png="kaprekar_hist.png", show=False):
    """Compute average & max steps and plot a histogram of counts.

    If `show` is True the histogram will be displayed interactively with `plt.show()`.
    """
    if not counts:
        print("No counts to analyze.")
        return
    avg = statistics.mean(counts)
    mx = max(counts)
    print(f"Tested {len(counts)} numbers (excluded repdigits).")
    print(f"Average steps to reach 6174: {avg:.3f}")
    print(f"Maximum steps: {mx}")

    # Find some example numbers that take the maximum number of steps
    nums_with_max = []
    for n in range(0, 10000):
        s = str(n).zfill(4)
        if is_repdigit(s):
            continue
        if steps_to_kaprekar(s) == mx:
            nums_with_max.append(s)
    print(f"Number(s) that take {mx} steps: {nums_with_max[:10]}{'...' if len(nums_with_max) > 10 else ''}")

    # Plot histogram
    plt.figure(figsize=(8, 5))
    hist_counts, hist_bins, _ = plt.hist(counts, bins=range(min(counts), max(counts) + 2), align='left', rwidth=0.8, color='C0')
    plt.xlabel("Steps to reach 6174")
    plt.ylabel("Count of 4-digit numbers")
    plt.title("Kaprekar Steps Distribution (4-digit numbers)")
    plt.grid(axis='y', alpha=0.75)

    # Annotate mean
    plt.axvline(avg, color='C1', linestyle='--', linewidth=1.5, label=f"Mean = {avg:.2f}")

    # Annotate maximum and some example numbers that hit the maximum
    y_max = max(hist_counts) if len(hist_counts) else 0
    try:
        idx_max = int(mx - min(counts))
        count_at_max = hist_counts[idx_max] if 0 <= idx_max < len(hist_counts) else 0
    except Exception:
        count_at_max = 0
    if count_at_max > 0:
        examples = nums_with_max[:5]
        examples_str = ', '.join(examples)
        plt.text(mx, count_at_max + y_max * 0.04, f"Max {mx} steps\nExamples: {examples_str}", ha='center', va='bottom', fontsize=8, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.6))

    plt.legend()
    plt.tight_layout()
    plt.savefig(out_png, dpi=150)
    print(f"Histogram saved to {out_png}")
    if show:
        try:
            plt.show()
        except Exception as e:
            print(f"Unable to display plot interactively: {e}")


def _sanity_checks():
    """Run a few sanity checks on known examples."""
    examples = {
        '3524': 3,
        '2111': 5,
        '8532': 1,  # 8532 -> 6174
    }
    for s, expected in examples.items():
        actual = steps_to_kaprekar(s)
        print(f"Check {s}: expected {expected}, got {actual}")


if __name__ == "__main__":
    _sanity_checks()
    counts, failures = compute_all()
    stats_and_plot(counts, show=True)
    if failures:
        print(f"Warning: {len(failures)} numbers failed to reach 6174 (e.g., '0000' or cycles). Sample: {failures[:5]}")