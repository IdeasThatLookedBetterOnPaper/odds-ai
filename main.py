#!/root/miniconda3/envs/odds-ai/bin/python

# ====DATA_GATHERING===================================================================================================
from data_gathering import manual_operations, data_collection

# manual_operations.download_events()
# manual_operations.print_events()
# manual_operations.download_markets()
# manual_operations.print_markets()
# manual_operations.print_odds('1.217890840')
# manual_tests.convert_to_new_models()

data_collection.collect_data(False)


# ====REINFORCEMENT_LEARNING===========================================================================================
# from reinforcement_learning import simulation

# simulation.simulate()
