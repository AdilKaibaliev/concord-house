from pathlib import Path

p = Path('index.html')
b = p.read_bytes()
if b"en:{core:'Economic engine of the system'" in b:
    raise SystemExit('English enhancement already present')

engine_marker = b"    }}\r\n  };\r\n  const stageNodes="
assert b.count(engine_marker) == 1, 'Engine insertion marker not unique'
engine_en = b"    }},\r\n    en:{core:'Economic engine of the system',stage:['Prove the economics','Working infrastructure','Expand directions','Next-generation institution'],idle:'Select a direction to see its role in the system.',nodes:{\r\n      warehouse:['Warehouse','Shared inventory in proven categories can reduce shortages and make purchasing more predictable.'],\r\n      logistics:['Logistics','Consolidated shipments and volume create a basis for more efficient delivery and direct importing.'],\r\n      production:['Production','Verified demand can eventually justify owned or contract production in selected categories.'],\r\n      investment:['Investment','Accumulated operating data and measurable economic results create a stronger foundation for new projects and capital.'],\r\n      education:['Education','The system can transfer practical skills in management, purchasing, finance and entrepreneurship to the next generation.'],\r\n      home:['Connection to home countries','Scale and capabilities can support durable business, educational and investment links with participants home countries.']\r\n    }}\r\n  };\r\n  const stageNodes="
b = b.replace(engine_marker, engine_en, 1)

quiz_marker = b"      },score:'\xd1\x8b\xd1\x80\xd0\xb0\xd1\x81\xd1\x82\xd0\xb0\xd0\xbb\xd0\xb4\xd1\x8b',answerStatus:['\xd0\xb6\xd0\xbe\xd0\xbe\xd0\xbf \xd0\xb6\xd0\xbe\xd0\xba','\xd1\x8b\xd1\x80\xd0\xb0\xd1\x81\xd1\x82\xd0\xb0\xd0\xbb\xd0\xb4\xd1\x8b','\xd1\x82\xd0\xb0\xd0\xba\xd1\x82\xd0\xbe\xd0\xbe','\xd1\x8b\xd1\x80\xd0\xb0\xd1\x81\xd1\x82\xd0\xb0\xd0\xbb\xd0\xb3\xd0\xb0\xd0\xbd \xd0\xb6\xd0\xbe\xd0\xba']\r\n    }\r\n  };\r\n\r\n  const fit=$('#fit');"
assert b.count(quiz_marker) == 1, 'Quiz insertion marker not unique'
quiz_en = """      },score:'ырасталды',answerStatus:['жооп жок','ырасталды','тактоо','ырасталган жок']
    },
    en:{
      eyebrow:'Three questions before a decision',title:'Check project readiness — and see what to do next.',lead:'Three short answers turn this section into a practical decision filter for a participant, partner or investor.',progress:'Question',of:'of',side:'Decision map',waiting:'Answer all three questions — your next step will appear here.',back:'← Back',restart:'Start again',labels:['Mechanism','Evidence','Rules'],states:['not answered','confirmed','needs clarification','not confirmed'],
      questions:[
        {q:'Do you understand how combined demand becomes economic leverage?',hint:'The logic should be clear without presentation language: recurring demand → shared purchasing position → measurable effect → infrastructure.',opts:[['Yes, the mechanism is clear',2,'I can explain it in my own words'],['I understand it partly',1,'I need to clarify some links'],['No, not yet',0,'I need to understand the model first']]},
        {q:'Do you have enough evidence to move forward?',hint:'This means verified volume, real SKUs, supplier quotes, pilot purchases and a measured economic result.',opts:[['Yes, the evidence is sufficient',2,'I am ready to assess the next stage'],['I need more data',1,'I want to see additional verification'],['No, not yet',0,'It is too early to decide']]},
        {q:'Are the participation and governance rules clear and acceptable to you?',hint:'Roles, operator authority, controls, decision rights, allocation of results and exit mechanics should be clear before scaling.',opts:[['Yes, the rules are clear',2,'Participation can be discussed'],['I have questions about the terms',1,'Some details need agreement'],['No, the rules do not work for me',0,'The terms should be changed or declined first']]}
      ],
      results:{
        model:{tag:'Understand the model first',title:'Do not move to an investment decision yet.',text:'The main gap is the economic mechanism itself. First understand how combined demand is formed and where the measurable effect comes from.',bullets:['Review the Model section','Explain the mechanism in your own words','Return to the test once the cause-and-effect chain is clear'],cta:'Review the model',href:'#model'},
        evidence:{tag:'Evidence is still needed',title:'The next step is to request and verify the facts.',text:'The mechanism is clear, but the evidence does not yet provide enough confidence. Test the numbers and the pilot rather than the idea.',bullets:['Verify recurring volume and key SKUs','Compare supplier quotes with actual purchases','Review the measured pilot result'],cta:'Check the economics',href:'#economics'},
        governance:{tag:'Clarify the rules',title:'The economics may work, but the decision now depends on governance.',text:'Before participating, resolve questions about authority, controls, allocation of results and exit.',bullets:['Review Board and Executive Management roles','Clarify controls and reporting','Agree the key participation rules'],cta:'Review governance',href:'#governance'},
        conditional:{tag:'Conditional readiness',title:'The project can be evaluated further, but one element still needs confirmation.',text:'You understand the foundation, but the flagged questions should be resolved before a substantive decision.',bullets:['List the remaining questions','Obtain the missing verification','Repeat the assessment after clarification'],cta:'Return to the economics',href:'#economics'},
        ready:{tag:'Ready for a substantive discussion',title:'You can move from reviewing the concept to a concrete discussion.',text:'Based on your answers, the mechanism is clear, the evidence is sufficient and the rules raise no fundamental objection.',bullets:['Define the role you may want to play','Discuss participation format and the next working step','Move to concrete project data and parameters'],cta:'Discuss the project',href:'mailto:lfc@legacyfidelity.com?subject=Concord%20House%20Project'}
      },score:'confirmed',answerStatus:['not answered','confirmed','clarify','not confirmed']
    }
  };

  const fit=$('#fit');""".replace('\n','\r\n').encode('utf-8')
b = b.replace(quiz_marker, quiz_en, 1)

assert b.count(b"en:{core:'Economic engine of the system'") == 1
assert b.count(b"eyebrow:'Three questions before a decision'") == 1
p.write_bytes(b)
print('Added English engine and quiz copy without rewriting unrelated bytes')
