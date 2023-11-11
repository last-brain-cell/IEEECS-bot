import asyncio
import datetime
import discord
from discord.ext import commands, tasks
from zoneinfo import ZoneInfo

questions = {
    "4": {
        "q": "Given an array which consists of only 0, 1 and 2. Sort the array without using any sorting algo",
        "l": "https://practice.geeksforgeeks.org/problems/sort-an-array-of-0s-1s-and-2s/0",
        "status": 0
    },
    "5": {
        "q": "Move all the negative elements to one side of the array ",
        "l": "https://www.geeksforgeeks.org/move-negative-numbers-beginning-positive-end-constant-extra-space/",
        "status": 0
    },
    "6": {
        "q": "Find the Union and Intersection of the two sorted arrays.",
        "l": "https://practice.geeksforgeeks.org/problems/union-of-two-arrays/0",
        "status": 0
    },
    "7": {
        "q": "Write a program to cyclically rotate an array by one.",
        "l": "https://practice.geeksforgeeks.org/problems/cyclically-rotate-an-array-by-one/0",
        "status": 0
    },
    "8": {
        "q": "find Largest sum contiguous Subarray [V. IMP]",
        "l": "https://practice.geeksforgeeks.org/problems/kadanes-algorithm/0",
        "status": 0
    },
    "9": {
        "q": "Minimise the maximum difference between heights [V.IMP]",
        "l": "https://practice.geeksforgeeks.org/problems/minimize-the-heights3351/1",
        "status": 0
    },
    "10": {
        "q": "Minimum no. of Jumps to reach end of an array",
        "l": "https://practice.geeksforgeeks.org/problems/minimum-number-of-jumps/0",
        "status": 0
    },
    "11": {
        "q": "Merge 2 sorted arrays without using Extra space.",
        "l": "https://practice.geeksforgeeks.org/problems/merge-two-sorted-arrays5135/1",
        "status": 0
    },
    "12": {
        "q": "Kadane's Algo [V.V.V.V.V IMP]",
        "l": "https://practice.geeksforgeeks.org/problems/kadanes-algorithm/0",
        "status": 0
    },
    "13": {
        "q": "Count Inversion",
        "l": "https://practice.geeksforgeeks.org/problems/inversion-of-array/0",
        "status": 0
    },
    "14": {
        "q": "find all pairs on integer array whose sum is equal to given number",
        "l": "https://practice.geeksforgeeks.org/problems/count-pairs-with-given-sum5022/1",
        "status": 0
    },
    "15": {
        "q": "find common elements In 3 sorted arrays",
        "l": "https://practice.geeksforgeeks.org/problems/common-elements1132/1",
        "status": 0
    },
    "16": {
        "q": "Rearrange the array in alternating positive and negative items with O(1) extra space",
        "l": "https://www.geeksforgeeks.org/rearrange-array-alternating-positive-negative-items-o1-extra-space/",
        "status": 0
    },
    "17": {
        "q": "Find if there is any subarray with sum equal to 0",
        "l": "https://practice.geeksforgeeks.org/problems/subarray-with-0-sum/0",
        "status": 0
    },
    "18": {
        "q": "Find factorial of a large number",
        "l": "https://practice.geeksforgeeks.org/problems/factorials-of-large-numbers/0",
        "status": 0
    },
    "19": {
        "q": "find maximum product subarray ",
        "l": "https://practice.geeksforgeeks.org/problems/maximum-product-subarray3604/1",
        "status": 0
    },
    "20": {
        "q": "Find longest coinsecutive subsequence",
        "l": "https://practice.geeksforgeeks.org/problems/longest-consecutive-subsequence/0",
        "status": 0
    },
    "21": {
        "q": "Given an array of size n and a number k, fin all elements that appear more than \" n/k \" times.",
        "l": "https://www.geeksforgeeks.org/given-an-array-of-of-size-n-finds-all-the-elements-that-appear-more-than-nk-times/",
        "status": 0
    },
    "22": {
        "q": "Maximum profit by buying and selling a share atmost twice",
        "l": "https://www.geeksforgeeks.org/maximum-profit-by-buying-and-selling-a-share-at-most-twice/",
        "status": 0
    },
    "23": {
        "q": "Find whether an array is a subset of another array",
        "l": "https://practice.geeksforgeeks.org/problems/array-subset-of-another-array/0",
        "status": 0
    },
    "24": {
        "q": "Find the triplet that sum to a given value",
        "l": "https://practice.geeksforgeeks.org/problems/triplet-sum-in-array/0",
        "status": 0
    },
    "25": {
        "q": "Trapping Rain water problem",
        "l": "https://practice.geeksforgeeks.org/problems/trapping-rain-water/0",
        "status": 0
    },
    "26": {
        "q": "Chocolate Distribution problem",
        "l": "https://practice.geeksforgeeks.org/problems/chocolate-distribution-problem/0",
        "status": 0
    },
    "27": {
        "q": "Smallest Subarray with sum greater than a given value",
        "l": "https://practice.geeksforgeeks.org/problems/smallest-subarray-with-sum-greater-than-x/0",
        "status": 0
    },
    "28": {
        "q": "Three way partitioning of an array around a given value",
        "l": "https://practice.geeksforgeeks.org/problems/three-way-partitioning/1",
        "status": 0
    },
    "29": {
        "q": "Minimum swaps required bring elements less equal K together",
        "l": "https://practice.geeksforgeeks.org/problems/minimum-swaps-required-to-bring-all-elements-less-than-or-equal-to-k-together/0",
        "status": 0
    },
    "30": {
        "q": "Minimum no. of operations required to make an array palindrome",
        "l": "https://practice.geeksforgeeks.org/problems/palindromic-array/0",
        "status": 0
    },
    "31": {
        "q": "Median of 2 sorted arrays of equal size",
        "l": "https://practice.geeksforgeeks.org/problems/find-the-median0527/1",
        "status": 0
    },
    "32": {
        "q": "Median of 2 sorted arrays of different size",
        "l": "https://www.geeksforgeeks.org/median-of-two-sorted-arrays-of-different-sizes/",
        "status": 0
    },
    "33": {
        "q": "Spiral traversal on a Matrix",
        "l": "https://practice.geeksforgeeks.org/problems/spirally-traversing-a-matrix/0",
        "status": 0
    },
    "34": {
        "q": "Find median in a row wise sorted matrix",
        "l": "https://practice.geeksforgeeks.org/problems/median-in-a-row-wise-sorted-matrix1527/1",
        "status": 0
    },
    "35": {
        "q": "Find row with maximum no. of 1's",
        "l": "https://practice.geeksforgeeks.org/problems/row-with-max-1s0023/1",
        "status": 0
    },
    "36": {
        "q": "Print elements in sorted order using row-column wise sorted matrix",
        "l": "https://practice.geeksforgeeks.org/problems/sorted-matrix/0",
        "status": 0
    },
    "37": {
        "q": "Maximum size rectangle",
        "l": "https://practice.geeksforgeeks.org/problems/max-rectangle/1",
        "status": 0
    },
    "38": {
        "q": "Find a specific pair in matrix",
        "l": "https://www.geeksforgeeks.org/find-a-specific-pair-in-matrix/",
        "status": 0
    },
    "39": {
        "q": "Rotate matrix by 90 degrees",
        "l": "https://www.geeksforgeeks.org/rotate-a-matrix-by-90-degree-in-clockwise-direction-without-using-any-extra-space/",
        "status": 0
    },
    "40": {
        "q": "Kth smallest element in a row-cpumn wise sorted matrix",
        "l": "https://practice.geeksforgeeks.org/problems/kth-element-in-matrix/1",
        "status": 0
    },
    "41": {
        "q": "Common elements in all rows of a given matrix",
        "l": "https://www.geeksforgeeks.org/common-elements-in-all-rows-of-a-given-matrix/",
        "status": 0
    },
    "42": {
        "q": "Check whether a String is Palindrome or not",
        "l": "https://practice.geeksforgeeks.org/problems/palindrome-string0817/1",
        "status": 0
    },
    "43": {
        "q": "Find Duplicate characters in a string",
        "l": "https://www.geeksforgeeks.org/print-all-the-duplicates-in-the-input-string/",
        "status": 0
    },
    "44": {
        "q": "Write a Code to check whether one string is a rotation of another",
        "l": "https://www.geeksforgeeks.org/a-program-to-check-if-strings-are-rotations-of-each-other/",
        "status": 0
    },
    "45": {
        "q": "Write a program to find the longest Palindrome in a string.[ Longest palindromic Substring]",
        "l": "https://practice.geeksforgeeks.org/problems/longest-palindrome-in-a-string/0",
        "status": 0
    },
    "46": {
        "q": "Find Longest Recurring Subsequence in String",
        "l": "https://practice.geeksforgeeks.org/problems/longest-repeating-subsequence/0",
        "status": 0
    },
    "47": {
        "q": "Print all Subsequences of a string.",
        "l": "https://www.geeksforgeeks.org/print-subsequences-string/",
        "status": 0
    },
    "48": {
        "q": "Print all the permutations of the given string",
        "l": "https://practice.geeksforgeeks.org/problems/permutations-of-a-given-string/0",
        "status": 0
    },
    "49": {
        "q": "Split the Binary string into two substring with equal 0\u2019s and 1\u2019s",
        "l": "https://www.geeksforgeeks.org/split-the-binary-string-into-substrings-with-equal-number-of-0s-and-1s/",
        "status": 0
    },
    "50": {
        "q": "Word Wrap Problem [VERY IMP].",
        "l": "https://practice.geeksforgeeks.org/problems/word-wrap/0",
        "status": 0
    },
    "51": {
        "q": "EDIT Distance [Very Imp]",
        "l": "https://practice.geeksforgeeks.org/problems/edit-distance3702/1",
        "status": 0
    },
    "52": {
        "q": "Find next greater number with same set of digits. [Very Very IMP]",
        "l": "https://practice.geeksforgeeks.org/problems/next-permutation/0",
        "status": 0
    },
    "53": {
        "q": "Balanced Parenthesis problem.[Imp]",
        "l": "https://practice.geeksforgeeks.org/problems/parenthesis-checker/0",
        "status": 0
    },
    "54": {
        "q": "Word break Problem[ Very Imp]",
        "l": "https://practice.geeksforgeeks.org/problems/word-break/0",
        "status": 0
    },
    "55": {
        "q": "Rabin Karp Algo",
        "l": "https://www.geeksforgeeks.org/rabin-karp-algorithm-for-pattern-searching/",
        "status": 0
    },
    "56": {
        "q": "KMP Algo",
        "l": "https://practice.geeksforgeeks.org/problems/longest-prefix-suffix2527/1",
        "status": 0
    },
    "57": {
        "q": "Convert a Sentence into its equivalent mobile numeric keypad sequence.",
        "l": "https://www.geeksforgeeks.org/convert-sentence-equivalent-mobile-numeric-keypad-sequence/",
        "status": 0
    },
    "58": {
        "q": "Minimum number of bracket reversals needed to make an expression balanced.",
        "l": "https://practice.geeksforgeeks.org/problems/count-the-reversals/0",
        "status": 0
    },
    "59": {
        "q": "Count All Palindromic Subsequence in a given String.",
        "l": "https://practice.geeksforgeeks.org/problems/count-palindromic-subsequences/1",
        "status": 0
    },
    "60": {
        "q": "Count of number of given string in 2D character array",
        "l": "https://www.geeksforgeeks.org/find-count-number-given-string-present-2d-character-array/",
        "status": 0
    },
    "61": {
        "q": "Search a Word in a 2D Grid of characters.",
        "l": "https://practice.geeksforgeeks.org/problems/find-the-string-in-grid/0",
        "status": 0
    },
    "62": {
        "q": "Boyer Moore Algorithm for Pattern Searching.",
        "l": "https://www.geeksforgeeks.org/boyer-moore-algorithm-for-pattern-searching/",
        "status": 0
    },
    "63": {
        "q": "Converting Roman Numerals to Decimal",
        "l": "https://practice.geeksforgeeks.org/problems/roman-number-to-integer/0",
        "status": 0
    },
    "64": {
        "q": "Number of flips to make binary string alternate",
        "l": "https://practice.geeksforgeeks.org/problems/min-number-of-flips/0",
        "status": 0
    },
    "65": {
        "q": "Find the first repeated word in string.",
        "l": "https://practice.geeksforgeeks.org/problems/second-most-repeated-string-in-a-sequence/0",
        "status": 0
    },
    "66": {
        "q": "Minimum number of swaps for bracket balancing.",
        "l": "https://practice.geeksforgeeks.org/problems/minimum-swaps-for-bracket-balancing/0",
        "status": 0
    },
    "67": {
        "q": "Find the longest common subsequence between two strings.",
        "l": "https://practice.geeksforgeeks.org/problems/longest-common-subsequence/0",
        "status": 0
    },
    "68": {
        "q": "Program to generate all possible valid IP addresses from given  string.",
        "l": "https://www.geeksforgeeks.org/program-generate-possible-valid-ip-addresses-given-string/",
        "status": 0
    },
    "69": {
        "q": "Write a program tofind the smallest window that contains all characters of string itself.",
        "l": "https://practice.geeksforgeeks.org/problems/smallest-distant-window/0",
        "status": 0
    },
    "70": {
        "q": "Rearrange characters in a string such that no two adjacent are same",
        "l": "https://practice.geeksforgeeks.org/problems/rearrange-characters/0",
        "status": 0
    },
    "71": {
        "q": "Minimum characters to be added at front to make string palindrome",
        "l": "https://www.geeksforgeeks.org/minimum-characters-added-front-make-string-palindrome/",
        "status": 0
    },
    "72": {
        "q": "Given a sequence of words, print all anagrams together",
        "l": "https://practice.geeksforgeeks.org/problems/k-anagrams-1/0",
        "status": 0
    },
    "73": {
        "q": "Find the smallest window in a string containing all characters of another string",
        "l": "https://practice.geeksforgeeks.org/problems/smallest-window-in-a-string-containing-all-the-characters-of-another-string/0",
        "status": 0
    },
    "74": {
        "q": "Recursively remove all adjacent duplicates",
        "l": "https://practice.geeksforgeeks.org/problems/consecutive-elements/0",
        "status": 0
    },
    "75": {
        "q": "String matching where one string contains wildcard characters",
        "l": "https://practice.geeksforgeeks.org/problems/wildcard-string-matching/0",
        "status": 0
    },
    "76": {
        "q": "Function to find Number of customers who could not get a computer",
        "l": "https://www.geeksforgeeks.org/function-to-find-number-of-customers-who-could-not-get-a-computer/",
        "status": 0
    },
    "77": {
        "q": "Transform One String to Another using Minimum Number of Given Operation",
        "l": "https://www.geeksforgeeks.org/transform-one-string-to-another-using-minimum-number-of-given-operation/",
        "status": 0
    },
    "78": {
        "q": "Check if two given strings are isomorphic to each other",
        "l": "https://practice.geeksforgeeks.org/problems/isomorphic-strings/0",
        "status": 0
    },
    "79": {
        "q": "Recursively print all sentences that can be formed from list of word lists",
        "l": "https://www.geeksforgeeks.org/recursively-print-all-sentences-that-can-be-formed-from-list-of-word-lists/",
        "status": 0
    },
    "80": {
        "q": "Find first and last positions of an element in a sorted array",
        "l": "https://practice.geeksforgeeks.org/problems/first-and-last-occurrences-of-x/0",
        "status": 0
    },
    "81": {
        "q": "Find a Fixed Point (Value equal to index) in a given array",
        "l": "https://practice.geeksforgeeks.org/problems/value-equal-to-index-value1330/1",
        "status": 0
    },
    "82": {
        "q": "square root of an integer",
        "l": "https://practice.geeksforgeeks.org/problems/count-squares3649/1",
        "status": 0
    },
    "83": {
        "q": "Maximum and minimum of an array using minimum number of comparisons",
        "l": "https://practice.geeksforgeeks.org/problems/middle-of-three2926/1",
        "status": 0
    },
    "84": {
        "q": "Optimum location of point to minimize total distance",
        "l": "https://www.geeksforgeeks.org/optimum-location-point-minimize-total-distance/",
        "status": 0
    },
    "85": {
        "q": "Find the repeating and the missing",
        "l": "https://practice.geeksforgeeks.org/problems/find-missing-and-repeating2512/1",
        "status": 0
    },
    "86": {
        "q": "find majority element",
        "l": "https://practice.geeksforgeeks.org/problems/majority-element/0",
        "status": 0
    },
    "87": {
        "q": "Searching in an array where adjacent differ by at most k",
        "l": "https://www.geeksforgeeks.org/searching-array-adjacent-differ-k/",
        "status": 0
    },
    "88": {
        "q": "find a pair with a given difference",
        "l": "https://practice.geeksforgeeks.org/problems/find-pair-given-difference/0",
        "status": 0
    },
    "89": {
        "q": "find four elements that sum to a given value",
        "l": "https://practice.geeksforgeeks.org/problems/find-all-four-sum-numbers/0",
        "status": 0
    },
    "90": {
        "q": "maximum sum such that no 2 elements are adjacent",
        "l": "https://practice.geeksforgeeks.org/problems/stickler-theif/0",
        "status": 0
    },
    "91": {
        "q": "Count triplet with sum smaller than a given value",
        "l": "https://practice.geeksforgeeks.org/problems/count-triplets-with-sum-smaller-than-x5549/1",
        "status": 0
    },
    "92": {
        "q": "merge 2 sorted arrays",
        "l": "https://practice.geeksforgeeks.org/problems/merge-two-sorted-arrays5135/1",
        "status": 0
    },
    "93": {
        "q": "print all subarrays with 0 sum",
        "l": "https://practice.geeksforgeeks.org/problems/zero-sum-subarrays/0",
        "status": 0
    },
    "94": {
        "q": "Product array Puzzle",
        "l": "https://practice.geeksforgeeks.org/problems/product-array-puzzle/0",
        "status": 0
    },
    "95": {
        "q": "Sort array according to count of set bits",
        "l": "https://practice.geeksforgeeks.org/problems/sort-by-set-bit-count/0",
        "status": 0
    },
    "96": {
        "q": "minimum no. of swaps required to sort the array",
        "l": "https://practice.geeksforgeeks.org/problems/minimum-swaps/1",
        "status": 0
    },
    "97": {
        "q": "K-th Element of Two Sorted Arrays",
        "l": "https://practice.geeksforgeeks.org/problems/k-th-element-of-two-sorted-array/0",
        "status": 0
    },
    "98": {
        "q": "Book Allocation Problem",
        "l": "https://practice.geeksforgeeks.org/problems/allocate-minimum-number-of-pages/0",
        "status": 0
    },
    "99": {
        "q": "Job Scheduling Algo",
        "l": "https://www.geeksforgeeks.org/weighted-job-scheduling-log-n-time/",
        "status": 0
    },
    "100": {
        "q": "Missing Number in AP",
        "l": "https://practice.geeksforgeeks.org/problems/arithmetic-number/0",
        "status": 0
    },
    "101": {
        "q": "Smallest number with atleastn trailing zeroes infactorial",
        "l": "https://practice.geeksforgeeks.org/problems/smallest-factorial-number5929/1",
        "status": 0
    },
    "102": {
        "q": "Painters Partition Problem:",
        "l": "https://practice.geeksforgeeks.org/problems/allocate-minimum-number-of-pages/0",
        "status": 0
    },
    "103": {
        "q": "Findthe inversion count",
        "l": "https://practice.geeksforgeeks.org/problems/inversion-of-array/0",
        "status": 0
    },
    "104": {
        "q": "Implement Merge-sort in-place",
        "l": "https://www.geeksforgeeks.org/in-place-merge-sort/",
        "status": 0
    },
    "105": {
        "q": "Write a Program to reverse the Linked List. (Both Iterative and recursive)",
        "l": "https://www.geeksforgeeks.org/reverse-a-linked-list/",
        "status": 0
    },
    "106": {
        "q": "Reverse a Linked List in group of Given Size. [Very Imp]",
        "l": "https://practice.geeksforgeeks.org/problems/reverse-a-linked-list-in-groups-of-given-size/1",
        "status": 0
    },
    "107": {
        "q": "Write a program to Detect loop in a linked list.",
        "l": "https://practice.geeksforgeeks.org/problems/detect-loop-in-linked-list/1",
        "status": 0
    },
    "108": {
        "q": "Write a program to Delete loop in a linked list.",
        "l": "https://practice.geeksforgeeks.org/problems/remove-loop-in-linked-list/1",
        "status": 0
    },
    "109": {
        "q": "Find the starting point of the loop.\u00a0",
        "l": "https://www.geeksforgeeks.org/find-first-node-of-loop-in-a-linked-list/",
        "status": 0
    },
    "110": {
        "q": "Remove Duplicates in a sorted Linked List.",
        "l": "https://practice.geeksforgeeks.org/problems/remove-duplicate-element-from-sorted-linked-list/1",
        "status": 0
    },
    "111": {
        "q": "Remove Duplicates in a Un-sorted Linked List.",
        "l": "https://practice.geeksforgeeks.org/problems/remove-duplicates-from-an-unsorted-linked-list/1",
        "status": 0
    },
    "112": {
        "q": "Write a Program to Move the last element to Front in a Linked List.",
        "l": "https://www.geeksforgeeks.org/move-last-element-to-front-of-a-given-linked-list/",
        "status": 0
    },
    "113": {
        "q": "Add \u201c1\u201d to a number represented as a Linked List.",
        "l": "https://practice.geeksforgeeks.org/problems/add-1-to-a-number-represented-as-linked-list/1",
        "status": 0
    },
    "114": {
        "q": "Add two numbers represented by linked lists.",
        "l": "https://practice.geeksforgeeks.org/problems/add-two-numbers-represented-by-linked-lists/1",
        "status": 0
    },
    "115": {
        "q": "Intersection of two Sorted Linked List.",
        "l": "https://practice.geeksforgeeks.org/problems/intersection-of-two-sorted-linked-lists/1",
        "status": 0
    },
    "116": {
        "q": "Intersection Point of two Linked Lists.",
        "l": "https://practice.geeksforgeeks.org/problems/intersection-point-in-y-shapped-linked-lists/1",
        "status": 0
    },
    "117": {
        "q": "Merge Sort For Linked lists.[Very Important]",
        "l": "https://practice.geeksforgeeks.org/problems/sort-a-linked-list/1",
        "status": 0
    },
    "118": {
        "q": "Quicksort for Linked Lists.[Very Important]",
        "l": "https://practice.geeksforgeeks.org/problems/quick-sort-on-linked-list/1",
        "status": 0
    },
    "119": {
        "q": "Check if a linked list is a circular linked list.",
        "l": "https://practice.geeksforgeeks.org/problems/circular-linked-list/1",
        "status": 0
    },
    "120": {
        "q": "Split a Circular linked list into two halves.",
        "l": "https://practice.geeksforgeeks.org/problems/split-a-circular-linked-list-into-two-halves/1",
        "status": 0
    },
    "121": {
        "q": "Write a Program to check whether the Singly Linked list is a palindrome or not.",
        "l": "https://practice.geeksforgeeks.org/problems/check-if-linked-list-is-pallindrome/1",
        "status": 0
    },
    "122": {
        "q": "Deletion from a Circular Linked List.",
        "l": "https://www.geeksforgeeks.org/deletion-circular-linked-list/",
        "status": 0
    },
    "123": {
        "q": "Reverse a Doubly Linked list.",
        "l": "https://practice.geeksforgeeks.org/problems/reverse-a-doubly-linked-list/1",
        "status": 0
    },
    "124": {
        "q": "Find pairs with a given sum in a DLL.",
        "l": "https://www.geeksforgeeks.org/find-pairs-given-sum-doubly-linked-list/",
        "status": 0
    },
    "125": {
        "q": "Count triplets in a sorted DLL whose sum is equal to given value \u201cX\u201d.",
        "l": "https://www.geeksforgeeks.org/count-triplets-sorted-doubly-linked-list-whose-sum-equal-given-value-x/",
        "status": 0
    },
    "126": {
        "q": "Sort a \u201ck\u201dsorted Doubly Linked list.[Very IMP]",
        "l": "https://www.geeksforgeeks.org/sort-k-sorted-doubly-linked-list/",
        "status": 0
    },
    "127": {
        "q": "Rotate DoublyLinked list by N nodes.",
        "l": "https://www.geeksforgeeks.org/rotate-doubly-linked-list-n-nodes/",
        "status": 0
    },
    "128": {
        "q": "Rotate a Doubly Linked list in group of Given Size.[Very IMP]",
        "l": "https://www.geeksforgeeks.org/reverse-doubly-linked-list-groups-given-size/",
        "status": 0
    },
    "129": {
        "q": "Flatten a Linked List",
        "l": "https://practice.geeksforgeeks.org/problems/flattening-a-linked-list/1",
        "status": 0
    },
    "130": {
        "q": "Sort a LL of 0's, 1's and 2's",
        "l": "https://practice.geeksforgeeks.org/problems/given-a-linked-list-of-0s-1s-and-2s-sort-it/1",
        "status": 0
    },
    "131": {
        "q": "Clone a linked list with next and random pointer",
        "l": "https://practice.geeksforgeeks.org/problems/clone-a-linked-list-with-next-and-random-pointer/1",
        "status": 0
    },
    "132": {
        "q": "Merge K sorted Linked list",
        "l": "https://practice.geeksforgeeks.org/problems/merge-k-sorted-linked-lists/1",
        "status": 0
    },
    "133": {
        "q": "Multiply 2 no. represented by LL",
        "l": "https://practice.geeksforgeeks.org/problems/multiply-two-linked-lists/1",
        "status": 0
    },
}


class Questions(commands.Cog, name="questions"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.send_questions.start()
        ...

    @tasks.loop(seconds=1)
    async def send_questions(self):
        now: datetime.datetime = datetime.datetime.now(ZoneInfo("Asia/Kolkata"))
        tomorrow = datetime.datetime(
            now.year, now.month, now.day, 22, 0, 0, 0, ZoneInfo("Asia/Kolkata")
        ) + datetime.timedelta(days=1)
        await asyncio.sleep((tomorrow - now).seconds)
        guild: discord.Guild = self.bot.get_guild(1171565156619268208)  # test Guild for now
        channel: discord.TextChannel = guild.get_channel(1172352404746936340)  # test channel for now
        try:
            # with open("../ques.json", "r") as file:
            idx = list(questions.keys())[0]
            question = questions[idx]["q"]
            link = questions[idx]["l"]
            # questions.pop(idx)

            embed = discord.Embed(color=0xffd500)
            embed.add_field(
                name="Question ", value=question, inline=False
            )
            embed.set_author(
                name="Click here to go to the Question",
                url=link
            )
            await channel.send(f"<@&1171834553661399130>\n❓Here is the Daily Problem❓\nThe Grind Continues..🎯",
                               embeds=[embed])
        except Exception as e:
            print(e)


async def setup(bot: commands.Bot):
    await bot.add_cog(Questions(bot))
