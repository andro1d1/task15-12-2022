from googlewriter import GoogleWriter
from amoCRM import AmoCrm
from datetime import date

def get_values(dict: dict)->list:
    """
    Return a list of dict values for GoogleWriter
    """
    return list(dict.values())

def main():

    writer = GoogleWriter()
    crm = AmoCrm()
    # events = crm.filter_entity_type("company") # one of [lead, contact, company, customer, task]
    
    events = crm.filter_date() # input date

    written_data = [[i.account_id, i.id, i.type, i.entity_id, 
                     i.entity_type, i.created_at.strftime("%H-%M-%S %B %d, %Y"), str(i.value_before), str(i.value_after)] for i in events]
    writer.write(written_data)


if __name__ == "__main__":
    main()