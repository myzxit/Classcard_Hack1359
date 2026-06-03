from main import main, parse_args

if __name__ == "__main__":
    args = parse_args()
    args.device = "mobile"
    main(args)
