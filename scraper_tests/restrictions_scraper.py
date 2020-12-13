import requests

response = requests.get("https://www.thrillophilia.com/mysore-tourist-places").text

restrictions = response.split("<ul>")[1].split("</ul>")[0].replace("</li>", "").strip("<li>").split("<li>")
quarantineRules = response.split("<ul>")[2].split("</ul>")[0].replace("</li>", "").strip("<li>").split("<li>")

print("Restrictions:")
print("\n".join(["> " + i.strip(".") + "." for i in restrictions]))

print()

print("Quarantine Rules:")
print("\n".join(["> " + i.strip(".") + "." for i in quarantineRules]))

print("\n")

# restrictions = [i.strip(".") + "." for i in restrictions]
