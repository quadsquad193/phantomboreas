def debug_print_results(results):
        # Uncomment to see the full results structure
        # import pprint
        # pprint.pprint(results)

        i = 0
        for plate in results:
            i += 1
            print("Plate #%d" % i)
            print("   %12s %12s" % ("Plate", "Confidence"))
            for candidate in plate['candidates']:
                prefix = "-"
                if candidate['matches_template']:
                    prefix = "*"

                print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))
